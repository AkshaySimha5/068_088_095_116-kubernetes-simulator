import click
import requests

@click.group()
def cli():
    pass

@cli.command()
@click.option('--api-server', default='http://localhost:5000')
@click.option('--cpu-cores', type=int, required=True)
def add_node(api_server, cpu_cores):
    response = requests.post(
        f"{api_server}/nodes",
        json={"cpu_cores": cpu_cores}
    )
    click.echo(response.json())

@cli.command()
@click.option('--api-server', default='http://localhost:5000')
def list_nodes(api_server):
    response = requests.get(f"{api_server}/nodes")
    for node in response.json():
        click.echo(f"Node {node['node_id']}: {node['cpu_cores']} cores, Status: {node['status']}")

@cli.command()
@click.option('--api-server', default='http://localhost:5000')
@click.option('--cpu-required', type=int, required=True)
def launch_pod(api_server, cpu_required):
    response = requests.post(
        f"{api_server}/pods",
        json={"cpu_required": cpu_required}
    )
    click.echo(response.json())

if __name__ == '__main__':
    cli()