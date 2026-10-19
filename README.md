# laudo-tecnico-web

Sistema de laudo técnico digital e diagnóstico técnico para assistência de informática e eletrônica.

## Integração por link com o aplicativo de diagnóstico

No aplicativo nativo, **Link do laudo** substitui a exportação de JSON. O técnico pode copiar o link ou abrir o laudo diretamente. Cada link leva a fase selecionada: **Análise → Técnico e parecer**, **Teste final → Testes**, mantendo a conferência do atendente manual. Fotos e prints permanecem na pasta da OS.

Ao abrir um link na mesma OS, a página pede confirmação e preserva a outra fase, data e campos já preenchidos que não vieram no envio. Linhas extras de discos são mescladas sem perder seus outros resultados. Uma OS diferente exige confirmação antes de substituir o conteúdo. Links anteriores e importações antigas continuam compatíveis.

No app, o link também pode ser aberto por **QR code** (celular ou PC do balcão) ou por **Enviar ao balcão**, que grava um atalho `.url` numa pasta compartilhada.

**Contrato de campos:** [`campos-laudo.json`](campos-laudo.json) lista os campos (`data-id`) e as opções de menu que o app preenche. O app embute uma cópia idêntica (`Diaginostico Tecnico/src/campos-laudo.json`). Ao renomear um campo ou mudar uma opção no `index.html`/`script.js`, atualize este arquivo e copie-o para o app. O teste do navegador falha se as cópias divergirem ou se um campo ou opção do contrato não existir na página.

O link é uma cópia dos dados, não uma sincronização em tempo real, e pode ser lido por quem o receber. Para atualizar o endereço online, publique `index.html` e `script.js` juntos. A atualização local não publica o GitHub Pages automaticamente.

Validação: execute os testes do projeto vizinho `Diaginostico Tecnico/tests/run.ps1` e depois `python tests/run-browser.py` nesta pasta. O teste abre Chrome/Edge sem interface e verifica links reais gerados pelo C#, incluindo Unicode, múltiplos discos, cancelamento, troca de OS e compatibilidade com links antigos.

O ecossistema é composto por:

1. **Laudo Técnico Digital (Web/Front-end):** Interface interativa para preenchimento de entrada, diagnóstico do técnico e conferência/testes com suporte a backup oculto dentro do PDF, link compartilhável, importação/exportação e impressão perfeita em 1 página A4.
2. **Suite de Automação de Diagnóstico (`script/`):** Script avançado em PowerShell para testes de bancada e automação de hardware.
3. **App de Diagnóstico (Em desenvolvimento):** O novo aplicativo nativo de diagnóstico técnico está sendo desenvolvido no repositório: [diagnostico-tecnico-cantao](https://github.com/IgVilhena/diagnostico-tecnico-cantao).

---

## 🔄 O Fluxo de Trabalho (Workflow da Loja)

A tabela do sistema espelha as etapas reais de atendimento na assistência:

1. **Entrada:** Preenchimento inicial no balcão. Registra o estado físico do equipamento (PC, Notebook ou TV), marcas de uso, peças presentes, se liga, etc.
2. **Técnico (Parecer Técnico):** Área do técnico para registrar peças defeituosas, testes efetuados, orçamentos, observações internas e parecer formal com barra de formatação (negrito, itálico, listas).
3. **Testes Finais:** Preenchido após o reparo na bancada. Garante que todos os componentes (rede, Wi-Fi, áudio, webcam, portas USB, teclado, bateria) foram validados antes da entrega.
4. **Checklist do Atendente (☑):** Caixas de validação para a equipe de balcão conferir cada item indicado pelo técnico, assegurando dupla checagem de qualidade.

---

## 💻 Funcionalidades do Sistema Web (`index.html`)

* **Tipos de Equipamento:** Alternância instantânea entre `PC`, `Notebook` e `TV`, exibindo apenas os componentes pertinentes.
* **Preenchimento em Lote:** Botões de preenchimento rápido ("Todos Funcionando", "Limpar", etc.).
* **Navegação Estilo Planilha:** Suporte completo a atalhos de teclado (`Tab`, `Ctrl + Setas`, `Alt + Setas`) para transitar entre células sem o mouse.
* **Persistência Local Automática:** Todos os dados são salvos em tempo real no `localStorage` do navegador para evitar perda de dados.
* **Importação & Exportação JSON:** Salve laudos completos em arquivos `.json` e importe-os a qualquer momento.
  * Suporte a JSON de **Diagnóstico Técnico** (preenche coluna Técnico e parecer).
  * Suporte a JSON de **Teste Final** (preenche a coluna Testes e marca os checkboxes).
* **Editor com Barra de Formatação:** Formatação rica no parecer técnico e observações de defeitos.
* **Assinatura do Atendente & Técnico:** Campos dedicados e persistentes para assinaturas de conferência.
* **Dark Mode & Impressão A4:** Tema escuro para operação diária e formatação automática em preto/branco comprimida para **exatamente 1 página A4** na impressão/PDF.

---

## ⚡ Script de Diagnóstico (`script/`)

Script PowerShell usado na bancada. Fica na raiz de um **pen drive (Ventoy)** junto das ferramentas portáteis e da pasta `OS/`, e é iniciado pelo `iniciar.bat`.

> [!IMPORTANT]
> Funciona no **Windows 10/11**. No **WinPE (Strelec) ainda não funciona**. O **novo app de diagnóstico** está sendo desenvolvido em [diagnostico-tecnico-cantao](https://github.com/IgVilhena/diagnostico-tecnico-cantao) para substituir o script e rodar nativamente.

Guia completo (menus, atalhos, estrutura do pen drive, **explicação do `config.json`**, WinPE): **[script/README.md](script/README.md)**.

### Resumo
* **Modos de teste:** Rápido, Completo, Completo + Estresse, Periféricos/Portas, Personalizado e **Teste Final**.
* **Ferramentas automatizadas:** HDDScan, CrystalDiskInfo, HDSentinel, HWiNFO, BatteryInfoView, KeyboardTest, UsbTreeView, Victoria e FurMark. A lista é configurável no `config.json`, sem mexer no código.
* **Prints por teclado:** `F9` (janela em foco), `F8` (tela inteira) e `Alt+F12`/`F12` para seguir. Fechar a janela no `[X]` também avança sozinho. Nenhum print é automático por tempo.
* **Teste Final:** testa periféricos e portas e preenche a coluna **TESTES** do laudo. Salva em uma OS existente (subpasta `teste final`) ou numa OS nova (`{OS} - teste final`).
* **Saídas por OS:** prints, textos de hardware, relatório HTML/PDF e JSONs para importar no laudo.

---

## 🚀 Como Executar

### Laudo Web
Abra **`index.html`** em qualquer navegador moderno (Edge, Chrome, Firefox). Não precisa de instalação nem servidor.

### Script de bancada
No Windows, execute **`script/iniciar.bat`** como **Administrador**, ou:
```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "script/diagnostico.ps1"
```
As ferramentas portáteis **não** estão no repositório: coloque cada uma em `script/Ferramentas/<pasta>` conforme o `config.json`.

