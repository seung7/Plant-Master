# Soil Moisture Sensor

## Hardware

| Components:                     |
| ------------------------------- |
| Nucleo stm32f410rb              |
| Capacitive Soil Moisture Sensor |
| 4LEDs                           |
| 220ohm resistor                 |

PA5: set to GPIO's out for board's Green LED </br>
PA1, PA4, PA6, PA7: set to GPIO's output for 4 external LEDs </br>
PA9: set to microcontroller's embedded 12bit ADC(analog to digital converter) </br>

<p align="center">
   <img src="Embedded/images/wiring diagram.png" width=650>
</p>

## Publishing data to AWS IoT

### AWS IoT setup

To send data to AWS, a raspberry pi 3 is used as an `AWS IoT thing`. For more setup info, read [the docs](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html). To set up from scratch:

- Register device as an `AWS IoT thing`
- Create an `AWS IoT policy`.
- Add a certificate to your `thing` and download auth-generated certificates/keys.
- Attach policy to the certificate.

### Email notifications setup

- Create a `topic` via Amazon SNS and add your email as subscription.
- Create an `AWS IoT rule` that defines the conditions to send an email, eg., moisture is below threshold.

### Install requirements

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
