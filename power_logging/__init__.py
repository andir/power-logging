import argparse
import datetime
import logging

import influxdb
import serial

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--device', type=str, default='/dev/ttyUSB0', help='serial file')
    parser.add_argument('--speed', type=int, default=19200, help='baud rate')
    parser.add_argument('--influx-host', type=str, default=False, help='influx db server')
    parser.add_argument('--influx-port', type=int, default=8086, help='influx db port')
    parser.add_argument('--influx-db', type=str, default='ffdasolardata', help='influx db name')

    parser.add_argument('--debug', default=False, action='store_true', help='enable debug')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.influx_host:

        logger.info('Configuring db connection')
        influx = influxdb.InfluxDBClient(host=args.influx_host, port=args.influx_port, database=args.influx_db)
    else:
        influx = None

    device = serial.Serial(port=args.device, baudrate=args.speed)

    data = {}
    while True:
        line = device.readline().decode('utf-8', errors='ignore')

        logger.debug(line)
        try:
            key, value = line.split('\t')
        except ValueError:
            logger.error('Failed to parse line: %s', line)
        else:
            logger.debug('key: %s, value: %s', key, value)
            try:
                data[key] = int(value.strip())
            except ValueError:
                pass

            if key == 'Checksum':

                json_body = [
                    {
                        "measurement": "mppt",
                        "tags": {},
                        "time": datetime.datetime.now().isoformat(),
                        "fields": data
                    }
                ]
                logger.debug(json_body)
                if influx:
                    influx.write_points(json_body)


if __name__ == "__main__":
    main()
