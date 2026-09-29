# -*- coding: utf-8 -*-
"""Sleepy Rain: a slow blue drizzle rendered on the reveil's LED loop.

The reveil's "top" LEDs form a single horizontal strip running around the
inside edge of the frosted lid, pointing inwards. There is no vertical axis,
so the falling-rain effect of the tower lamp cannot be reproduced as-is.

Instead this is a one-dimensional adaptation: every drop lands at a random
position on the loop and launches two wavefronts that travel both ways around
it (wrapping past the ends) and deposit energy into a slowly decaying buffer.
It reads as raindrops rippling across the lid, with long soft trails, a dim
blue palette, a burst-then-pause drop cadence and rare, gentle flashes.

Ported from tower-lamp's ``SleepyRainStrategy`` (the ``SLEEPY_RAIN`` preset).
"""

import logging
import math
import random
import time

import config
from StoppablePausableThread import StoppablePausableThread

try:
    from neopixel import Color
except ImportError:  # lets the module be imported on a non-RPi dev host
    def Color(r, g, b):
        return (int(r) << 16) | (int(g) << 8) | int(b)


# Palette lifted from tower-lamp's SleepyRainStrategy (dim blues).
PALETTE = [
    (35, 75, 185),
    (45, 95, 200),
    (55, 115, 210),
    (65, 130, 220),
    (78, 150, 228),
    (40, 85, 195),
]

DEFAULT_BRIGHTNESS = 0.55
DEFAULT_FPS = 30
DEFAULT_DURATION = 1800.0  # 30 min sleep session; <= 0 runs until stopped
DEFAULT_FADE_OUT = 20.0

FADE_HALF_LIFE_S = 0.7  # trail persistence: time for a lit cell to halve

RIPPLE_SPEED = 3.5  # leds / second
RIPPLE_LIFE_S = 5.5
RIPPLE_SIGMA = 1.3  # ring half-width, in leds
RIPPLE_AMPLITUDE = 1.0

BURST_MIN = 1
BURST_MAX = 2
BURST_SPACING_S = 0.45
PAUSE_MIN_S = 1.1
PAUSE_MAX_S = 2.2
MAX_DROPS = 3

FLASH_INTERVAL_S = 24.0
FLASH_DURATION_S = 0.55
FLASH_BOOST = 0.12

AMBIENT_RGB = (2, 5, 16)


class _Ripple(object):
    __slots__ = ("center", "age", "color")

    def __init__(self, center, color):
        self.center = center
        self.age = 0.0
        self.color = color


class SleepyRain(StoppablePausableThread):
    def __init__(self, light, duration=DEFAULT_DURATION, brightness=DEFAULT_BRIGHTNESS,
                 fps=DEFAULT_FPS, fade_out=DEFAULT_FADE_OUT):
        super(SleepyRain, self).__init__()
        self.light = light

        self.offset = light.top_offset
        self.length = light.top_strip_length + light.top_center_length

        self.brightness = brightness
        self.frame_time = 1.0 / float(fps)
        self.fade_out = fade_out

        self.duration = duration if (duration and duration > 0) else None
        self._elapsed = 0.0

        self._grid = [[0.0, 0.0, 0.0] for _ in range(self.length)]
        self._ripples = []

        self._last_tick = 0.0
        self._next_drop_at = 0.0
        self._burst_remaining = 0
        self._next_flash_at = 0.0
        self._flash = 0.0
        self._flash_led = -1

    def run(self):
        logging.info("LIGHT : Sleepy Rain mode (%d leds)", self.length)
        now = time.monotonic()
        self._last_tick = now
        self._next_drop_at = now
        self._burst_remaining = 0
        self._next_flash_at = now + FLASH_INTERVAL_S
        super(SleepyRain, self).run()

    def work(self):
        now = time.monotonic()
        dt = min(max(now - self._last_tick, 0.0), 0.5)
        self._last_tick = now

        self._elapsed += dt
        out_scale = 1.0
        if self.duration is not None:
            remaining = self.duration - self._elapsed
            if remaining <= self.fade_out:
                out_scale = max(0.0, remaining / self.fade_out)
                if remaining <= 0.0:
                    self._blackout()
                    self.stop()
                    return

        self._update(dt, now)
        self._render(out_scale)

        time.sleep(self.frame_time)

    def _update(self, dt, now):
        fade = math.pow(0.5, dt / FADE_HALF_LIFE_S) if dt > 0 else 1.0
        for cell in self._grid:
            cell[0] *= fade
            cell[1] *= fade
            cell[2] *= fade

        if self._flash > 0.0:
            self._flash = max(0.0, self._flash - dt / FLASH_DURATION_S)

        if now >= self._next_drop_at and len(self._ripples) < MAX_DROPS:
            self._spawn_drop(now)

        if now >= self._next_flash_at:
            self._flash = 1.0
            self._flash_led = random.randrange(self.length)
            self._next_flash_at = now + FLASH_INTERVAL_S * (0.6 + random.random() * 0.8)

        for ripple in list(self._ripples):
            ripple.age += dt
            if ripple.age >= RIPPLE_LIFE_S:
                self._ripples.remove(ripple)
                continue
            self._deposit(ripple)

    def _spawn_drop(self, now):
        self._ripples.append(_Ripple(random.randrange(self.length), random.choice(PALETTE)))

        if self._burst_remaining <= 0:
            self._burst_remaining = random.randint(BURST_MIN, BURST_MAX)
        self._burst_remaining -= 1
        if self._burst_remaining > 0:
            self._next_drop_at = now + BURST_SPACING_S
        else:
            self._next_drop_at = now + PAUSE_MIN_S + random.random() * (PAUSE_MAX_S - PAUSE_MIN_S)

    def _deposit(self, ripple):
        radius = RIPPLE_SPEED * ripple.age
        decay = max(0.0, 1.0 - ripple.age / RIPPLE_LIFE_S)
        amplitude = RIPPLE_AMPLITUDE * decay * decay
        sigma2 = 2.0 * RIPPLE_SIGMA * RIPPLE_SIGMA
        color = ripple.color
        n = self.length

        for i in range(n):
            d = abs(i - ripple.center)
            d = min(d, n - d)
            intensity = math.exp(-((d - radius) ** 2) / sigma2) * amplitude
            if intensity <= 0.002:
                continue
            # Per-cell max (like the tower's stamp) keeps overlapping ripples
            # from summing into a saturated white; the persistence buffer
            # still leaves a decaying trail behind the wavefront.
            cell = self._grid[i]
            r = color[0] * intensity
            g = color[1] * intensity
            b = color[2] * intensity
            if r > cell[0]:
                cell[0] = r
            if g > cell[1]:
                cell[1] = g
            if b > cell[2]:
                cell[2] = b

    def _render(self, out_scale):
        scale = self.brightness * out_scale
        boost = 1.0 + self._flash * FLASH_BOOST
        ar, ag, ab = AMBIENT_RGB
        base = self.offset

        with config.strip_lock:
            for i, cell in enumerate(self._grid):
                r = cell[0] * boost + ar
                g = cell[1] * boost + ag
                b = cell[2] * boost + ab
                if i == self._flash_led and self._flash > 0.0:
                    extra = self._flash * 40.0
                    r += extra * 0.6
                    g += extra
                    b += extra * 1.4
                r = int(min(255.0, r * scale))
                g = int(min(255.0, g * scale))
                b = int(min(255.0, b * scale))
                self.light.strip.setPixelColor(base + i, Color(r, g, b))
            self.light.strip.show()

    def _blackout(self):
        with config.strip_lock:
            for i in range(self.length):
                self.light.strip.setPixelColor(self.offset + i, Color(0, 0, 0))
            self.light.strip.show()
