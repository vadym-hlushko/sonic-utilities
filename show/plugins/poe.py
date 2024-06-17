"""
Show CLI plugin for the SONiC Power over Ethernet feature.
Part of this file is auto-generated by sonic-cli-gen tool.
"""

import click
import tabulate
import natsort
import utilities_common.cli as clicommon


PORT_STR = 'Ethernet'

POE_PORT = 'POE_PORT'

POE_PORT_STATE = 'POE_PORT_STATE'
FP_PORT = 'fp_port'
CLASS = 'class'
CURRENT = 'current'
ENABLED = 'enabled'
PRIORITY = 'priority'
PROTOCOL = 'protocol'
PWR_CONSUMP = 'pwr_consump'
PWR_LIMIT = 'pwr_limit'
STATUS = 'status'
VOLTAGE = 'voltage'
DELIVERING = 'delivering'
SEARCHING = 'searching'
TRUE = 'true'
FALSE = 'false'
N_A = 'N/A'

# Headers
PORT_H = 'Port'
STATUS_H = 'Status'
EN_DIS_H = 'En/Dis'
PRIORITY_H = 'Priority'
PROTOCOL_H = 'Protocol'
CLASS_H = 'Class'
PWR_CONSUMP_H = 'PWR Consump'
PWR_LIMIT_H = 'PWR Limit'
VOLTAGE_H = 'Voltage'
CURRENT_H = 'Current'
TOTAL_POE_PORTS_H = 'Total PoE Ports'
TOTAL_POWER_H = 'Total Power'
TOTAL_CONSUMPTION_H = 'Power Consumption'
POWER_AVAILABLE_H = 'Power Available'
PLATFORM_SUPPORTED_H = 'Platform supported'
PSE_STATUS_H = 'PSE status'
PSE_TEMP_H = 'PSE temperature'
PSE_SW_VER_H = 'PSE SW ver'
PSE_HW_VER_H = 'PSE HW ver'


def format_attr_value(entry, attr):
    """ Helper that formats attribute to be presented in the table output.

    Args:
        entry (Dict[str, str]): CONFIG DB entry configuration.
        attr (Dict): Attribute metadata.

    Returns:
        str: fomatted attribute value.
    """

    if attr["is-leaf-list"]:
        return "\n".join(entry.get(attr["name"], []))
    return entry.get(attr["name"], "N/A")


def format_group_value(entry, attrs):
    """ Helper that formats grouped attribute to be presented in the table output.

    Args:
        entry (Dict[str, str]): CONFIG DB entry configuration.
        attrs (List[Dict]): Attributes metadata that belongs to the same group.

    Returns:
        str: fomatted group attributes.
    """

    data = []
    for attr in attrs:
        if entry.get(attr["name"]):
            data.append((attr["name"] + ":", format_attr_value(entry, attr)))
    return tabulate.tabulate(data, tablefmt="plain")


def get_value(value):
    return value if value not in [None, ''] else N_A


def format_value(key, value):
    units = {
        CURRENT: 'A',
        PWR_CONSUMP: 'W',
        PWR_LIMIT: 'W',
        VOLTAGE: 'V'
    }

    formatted_value = get_value(value)
    if formatted_value != N_A and key in units:
        return f"{float(formatted_value):.3f} {units[key]}"
    return formatted_value


@click.group(
    name="poe",
    cls=clicommon.AliasedGroup
)
def poe():
    """  Show PoE (Power over Ethernet) feature information """
    pass


# 'interface' subcommand ("show poe interface ...")
@poe.group(
    name="interface",
    cls=clicommon.AliasedGroup
)
def interface():
    """  Show PoE interface information """
    pass


# 'configuration' subcommand ("show poe interface configuration")
@interface.group(
    name="configuration",
    cls=clicommon.AliasedGroup,
    invoke_without_command=True
)
@clicommon.pass_db
def configuration(db):
    """  Show PoE configuration from Config DB """

    header = [
        PORT_H,
        EN_DIS_H,
        PWR_LIMIT_H,
        PRIORITY_H
    ]

    body = []

    table = db.cfgdb.get_table(POE_PORT)
    for key in natsort.natsorted(table):
        entry = table[key]
        if not isinstance(key, tuple):
            key = (key,)

        row = [*key] + [
            format_attr_value(
                entry,
                {'name': 'enabled',
                 'description': 'PoE status on port. [enable/disable]',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'power-limit',
                 'description': 'Power limit on PoE port. [0..999]',
                 'is-leaf-list': False,
                 'is-mandatory': True,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'priority',
                 'description': 'Port priority level. [crit/high/low]',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
        ]

        body.append(row)

    click.echo(tabulate.tabulate(body, header))


# 'state' subcommand ("show poe interface state")
@interface.command()
@click.argument(
    "ifname",
    required=False
)
@clicommon.pass_db
def state(db, ifname):
    """  Show details of the PoE interface  """

    state_db = db.db.STATE_DB
    delimiter = db.db.get_db_separator(state_db)

    if ifname is None:
        poe_port_keys = db.db.keys(state_db, f"{POE_PORT_STATE}{delimiter}*")
    else:
        if not ifname.startswith(PORT_STR):
            click.echo("Invalid ifname argument")
            return
        poe_port_keys = db.db.keys(state_db, f"{POE_PORT_STATE}{delimiter}{ifname}")

    if poe_port_keys is None or not poe_port_keys:
        click.echo(f"Interface <{ifname}> does not have PoE configuration")
        return

    header = [
        PORT_H,
        STATUS_H,
        EN_DIS_H,
        PRIORITY_H,
        PROTOCOL_H,
        CLASS_H,
        PWR_CONSUMP_H,
        PWR_LIMIT_H,
        VOLTAGE_H,
        CURRENT_H
    ]

    body = []

    for key in poe_port_keys:
        fv_list = db.db.get_all(state_db, key)
        row = [
            key.split(delimiter)[1],
            {TRUE: DELIVERING, FALSE: SEARCHING, N_A: N_A} [get_value(fv_list.get(STATUS))],
            get_value(fv_list.get(ENABLED)),
            get_value(fv_list.get(PRIORITY)),
            get_value(fv_list.get(PROTOCOL)),
            get_value(fv_list.get(CLASS)),
            format_value(PWR_CONSUMP, fv_list.get(PWR_CONSUMP)),
            format_value(PWR_LIMIT, fv_list.get(PWR_LIMIT)),
            format_value(VOLTAGE, fv_list.get(VOLTAGE)),
            format_value(CURRENT, fv_list.get(CURRENT))
        ]
        body.append(row)

    click.echo(tabulate.tabulate(body, header))


def register(cli):
    """ Register new CLI nodes in root CLI.

    Args:
        cli (click.core.Command): Root CLI node.
    Raises:
        Exception: when root CLI already has a command
                   we are trying to register.
    """

    cli_node = poe
    if cli_node.name in cli.commands:
        raise Exception(f"{cli_node.name} already exists in CLI")
    cli.add_command(poe)
