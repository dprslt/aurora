# Aurora

## Prérequis

### Packages python : 
```
python3-rpi.gpio
python3-numpy
python3-paho-mqtt
```

### Librairies Neo pixels

https://github.com/jgarff/rpi_ws281x

Il faut installler les dépendances et cette librairie en utilisant python 3

## Utilisation

Instalation et lancement du daemon

```
./install.sh
```

## Integration MQTT (Home Assistant)

Le daemon expose un device light (couleur + intensité) via la découverte MQTT de Home Assistant.

1. Créer un utilisateur sur le broker (Settings -> Mosquitto -> Users)
2. Créer le fichier de configuration :

```
sudo mkdir -p /etc/aurora
sudo tee /etc/aurora/mqtt.conf << EOM
MQTT_HOST=192.168.17.150
MQTT_PORT=1883
MQTT_USER=aurora
MQTT_PASS=mon_mot_de_passe
EOM
sudo chmod 600 /etc/aurora/mqtt.conf
```

3. Redémarrer le daemon : `sudo systemctl restart aurora`

Options optionnelles dans `mqtt.conf` : `MQTT_BASE_TOPIC` (défaut `aurora/light`),
`MQTT_DISCOVERY_PREFIX` (défaut `homeassistant`). Les variables d'environnement
`MQTT_*` sont utilisées en secours si le fichier est absent.

L'entité `light.aurora` apparaît automatiquement dans Home Assistant (découverte MQTT).

## Effet Sleepy Rain (endormissement)

Pluie bleue apaisante rendue sur le ruban du couvercle. Comme ce ruban forme une
**boucle horizontale** (pas de chute verticale possible), l'effet est adapté en
1D : une goutte tombe à une position aléatoire et deux fronts d'onde partent dans
les deux sens autour de la boucle, se croisent et s'estompent, avec une traînée
persistante, un cadencement par rafales suivies de pauses, une palette bleue
sombre et de rares flashs doux. Les réglages (palette, vitesse, densité,
luminosité) sont en tête de `src/strategies/light/SleepyRain.py`.

Déclenchement :

- **Bouton 2** (navigation des modes) : un appui fait défiler les modes, dont
  `rAi ` (Sleepy Rain) — mode continu.
- **REST** : `POST /light/sleepy_rain` avec l'option `?duration=<secondes>`
  (`0` = sans minuterie). Par défaut `1800` s (30 min), puis fondu vers l'extinction.
- **MQTT / Home Assistant** : bouton `Sleepy Rain` et effet `sleepy_rain` sur
  `light.aurora`.

La durée des sessions MQTT/REST est réglable via `SLEEPY_RAIN_DURATION` (secondes,
`0` = continu) dans `/etc/aurora/mqtt.conf`.

