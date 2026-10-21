"""Gera "Diagnóstico Técnico.HTML" (o laudo em um arquivo só) a partir de index.html, style.css e script.js.

Rode depois de mudar o site:   python gerar-arquivo-unico.py
Conferir se está atualizado:   python gerar-arquivo-unico.py --check   (o teste do navegador faz isso)

O arquivo único continua buscando na internet a fonte, os ícones e o pdf.js, como o site.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAIDA = ROOT / 'Diagnóstico Técnico.HTML'
AVISO = '<!-- Gerado por gerar-arquivo-unico.py a partir de index.html, style.css e script.js. Não edite à mão. -->'


def gerar():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    css = (ROOT / 'style.css').read_text(encoding='utf-8')
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    if re.search(r'</script', js, re.I) or re.search(r'</style', css, re.I):
        raise SystemExit('script.js ou style.css contém </script> ou </style>: o arquivo único quebraria.')

    html, n_css = re.subn(r'<link rel="stylesheet" href="style\.css(\?v=\d+)?"\s*/?>',
                          lambda m: '<style>\n' + css.rstrip() + '\n  </style>', html)
    html, n_js = re.subn(r'<script src="script\.js(\?v=\d+)?"></script>',
                         lambda m: '<script>\n' + js.rstrip() + '\n  </script>', html)
    if n_css != 1 or n_js != 1:
        raise SystemExit('Não encontrei <link href="style.css"> e <script src="script.js"> no index.html.')
    return html.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n' + AVISO, 1)


def main():
    novo = gerar()
    if '--check' in sys.argv:
        atual = SAIDA.read_text(encoding='utf-8') if SAIDA.exists() else ''
        if atual != novo:
            raise SystemExit('Diagnóstico Técnico.HTML está desatualizado: rode  python gerar-arquivo-unico.py')
        print('Diagnóstico Técnico.HTML está atualizado.')
        return
    SAIDA.write_text(novo, encoding='utf-8', newline='\n')
    print('Gerado:', SAIDA.name, f'({len(novo.encode("utf-8")) // 1024} KB)')


if __name__ == '__main__':
    main()
