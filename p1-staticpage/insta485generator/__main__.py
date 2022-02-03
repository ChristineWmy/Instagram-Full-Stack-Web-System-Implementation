"""Build static HTML site from directory of HTML templates and plain files."""
import pathlib
import json
import shutil
import click
import jinja2


@click.command()
@click.option('-o', '--output', help='Output directory.', type=click.Path())
@click.option('-v', '--verbose', is_flag=True, help='Print more output.')
@click.argument('INPUT_DIR', type=click.Path(exists=True))
def main(input_dir=None, output=None, verbose=False):
    """Templated static website generator."""
    # Convert str to Path object
    input_dir = pathlib.Path(input_dir)
    # The location of templates
    template_dir = input_dir/'templates'

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )

    # Load json object
    json_info = json.load(open(input_dir/'config.json'))

    if output:
        output_dir = pathlib.Path(output)
    else:
        output_dir = input_dir/'html'

    static_dir = input_dir/'static'
    if static_dir.is_dir():
        # Copy directory to the output directory
        shutil.copytree(static_dir, output_dir)
        # breakpoint()
        if verbose:
            print('Copied {} -> {}'.format(str(static_dir), str(output_dir)))
    if not output_dir.is_dir():
        output_dir.mkdir()
    for item in json_info:
        template = template_env.get_template(item['template'])
        url = item['url'].lstrip('/')
        context = item['context']
        output_dir_url = output_dir/url
        if not output_dir_url.is_dir():
            output_dir_url.mkdir(mode=0o777, parents=True)
        output_path = output_dir_url/'index.html'

        # Creat a file at this given path
        output_path.touch()
        output_path.write_text(template.render(context))
        if verbose:
            print('Rendered {} -> {}'.
                  format(item['template'], str(output_path)))


if __name__ == "__main__":
    main()
