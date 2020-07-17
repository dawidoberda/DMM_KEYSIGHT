import dmm_keysight as dk
import click
from configparser import ConfigParser
import logging

@click.command()
@click.option('-m', '--measure', help='Arguments:res - 2 wire resistance')
@click.option('-a', '--address', default='TCPIP0::K-34461A-09586.local::hislip0::INSTR', help='Argument: Visa address of dmm. Default is TCPIP0::K-34461A-09586.local::hislip0::INSTR')
@click.option('-l', '--limits', default='0', help='Set limits for measurement [upper,lower]')
def measure(measure, address, limits):
    dmm = dk.DMM()
    judgment = None
    measured_type = None
    measured_value = None
    lower_limit = None
    upper_limit = None
    limit_set = False

    connection_successful = dmm.connect(address)
    click.echo(connection_successful)
    if connection_successful:
        click.echo("Connection succesful")
        dmm.identificator()
    else:
        click.echo("Cannot connect to device")

    if measure == "res":
        click.echo("Measuring two wire resistance...")
        measured_value = dmm.measure_resistance_2wire()
        click.echo(f'Measured resistance value is : {measured_value}')
        measured_type = '2 wire resistance'

    #Limits check
    if limits == "0":
        click.echo('no limits set')
    else:
        try:
            lower_limit, upper_limit = str(limits).split(',')
            lower_limit = float(lower_limit)
            upper_limit = float(upper_limit)
            click.echo(f'Lower limit : {lower_limit}')
            click.echo(f'Uppper limit : {upper_limit}')
            limit_set = True
            #Judgment
            measured_value = float(measured_value)
            if measured_value >= lower_limit and measured_value <= upper_limit:
                judgment = "Pass"
            else:
                judgment = "Fail"

            click.echo(judgment)

        except ValueError as ve:
            click.echo("Wrong input. Please try to set limits separated using comma. Example: 500,700")
            click.echo(str(ve))
        except:
            click.echo("Other error occur")

    #filling results.ini
    results = ConfigParser()

    results['output'] = {
        'Measurement_type': measured_type,
        'Measurement_value': measured_value,
        'Limits_set': limit_set,
        'Lower_limit': lower_limit,
        'Upper_limit': upper_limit,
        'Judgment': judgment
    }

    with open('output/results.ini', 'w') as f:
        results.write(f)


if __name__=="__main__":
    measure()