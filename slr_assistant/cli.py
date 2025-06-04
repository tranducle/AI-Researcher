import click
from pathlib import Path
from .project import SLRProject, Study
from .documents import store_pdf, extract_pdf_text
from .llm import query_llm
from .prisma import export_flow_diagram


@click.group()
def cli():
    """CLI for the SLR assistant."""


@cli.command()
@click.argument('project_path')
def init(project_path):
    """Create a new SLR project."""
    path = Path(project_path)
    SLRProject(path).close()
    click.echo(f"Project initialized at {path}")


@cli.command()
@click.argument('project_path')
@click.argument('csv_file', type=click.Path(exists=True))
def import_records(project_path, csv_file):
    """Import study records from a CSV file."""
    import pandas as pd

    project = SLRProject(Path(project_path))
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        study = Study(title=row.get('title', ''), authors=row.get('authors', ''), abstract=row.get('abstract', ''), doi=row.get('doi'))
        project.add_study(study)
    project.close()
    click.echo(f"Imported {len(df)} records")


@cli.command()
@click.argument('project_path')
@click.argument('study_id', type=int)
@click.argument('pdf_file', type=click.Path(exists=True))
def add_pdf(project_path, study_id, pdf_file):
    """Attach a PDF file to a study."""
    project = SLRProject(Path(project_path))
    dest = store_pdf(Path(project_path), Path(pdf_file))
    cur = project.conn.cursor()
    cur.execute("UPDATE studies SET pdf_path = ? WHERE id = ?", (str(dest), study_id))
    project.conn.commit()
    project.close()
    click.echo("PDF stored")


@cli.command()
@click.argument('project_path')
@click.argument('study_id', type=int)
def extract(project_path, study_id):
    """Extract text from a study PDF."""
    project = SLRProject(Path(project_path))
    cur = project.conn.cursor()
    cur.execute("SELECT pdf_path FROM studies WHERE id = ?", (study_id,))
    row = cur.fetchone()
    if not row or not row[0]:
        click.echo("PDF not found")
        return
    text = extract_pdf_text(Path(row[0]))
    click.echo(text[:1000])
    project.close()


@cli.command()
@click.argument('project_path')
@click.argument('question')
@click.option('--provider', default='openai')
@click.option('--api_key', default=None)
@click.option('--model', default='gpt-3.5-turbo')
def ask(project_path, question, provider, api_key, model):
    """Ask a question about all included study abstracts."""
    project = SLRProject(Path(project_path))
    studies = project.list_studies(included=True)
    context = "\n\n".join(s.abstract for s in studies)
    prompt = f"Answer the question based on the following abstracts:\n{context}\n\nQuestion: {question}"
    answer = query_llm(provider, prompt, api_key=api_key, model=model)
    click.echo(answer)
    project.close()


@cli.command()
@click.argument('project_path')
@click.argument('output_file')
def prisma(project_path, output_file):
    """Export PRISMA flow diagram."""
    project = SLRProject(Path(project_path))
    export_flow_diagram(project.prisma, output_file)
    project.close()
    click.echo(f"PRISMA flow diagram saved to {output_file}")


if __name__ == '__main__':
    cli()
