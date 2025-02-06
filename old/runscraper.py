from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.progress import Progress
from core.scraper import WebScraper
import config.settings as settings

def main():
    scraper = WebScraper(settings.LINKS_FILE)
    links = scraper.links
    linkstotais = len(links)
    linksquebrados = 0
    linksfuncionando = 0

    console = Console()

    with ThreadPoolExecutor(max_workers=3) as executor:
        with Progress(console=console) as progress:
            task = progress.add_task("Processando links...", total=linkstotais)
            futures = []
            for link in links:
                futures.append(executor.submit(scraper.processar_link, link))

            for future in futures:
                try:
                    status_ok, dados = future.result()
                    if status_ok:
                        linksfuncionando += 1
                    else:
                        linksquebrados += 1
                    progress.update(task, advance=1, description=f"[SUCESS: {linksfuncionando} | FAIL: {linksquebrados}]")
                except Exception as e:
                    linksquebrados += 1
                    console.print(f"[red]Erro ao processar link: {e}[/red]")

    console.print(f"SUCESS: {linksfuncionando} | FAIL: {linksquebrados}", style="bold green")

if __name__ == '__main__':
    main()
