# AIcast
### Podcast automatizado utilizando Python e APIs da Open AI e Google AI Studio (Gemini Pro)

**Visite o cana [Scintilla Hub](https://www.youtube.com/@scintillahub) no YouTube**

## Requisitos
O projeto é desenvolvido e testado em ambiente Windows, podendo ser facilmente utilizando no Linux. É necessário ter o [Git](https://git-scm.com/download/win) instalado no Windows. Para o desenvolvimento utilizou-se o [Visual Studio Code](https://code.visualstudio.com/download) com a linguagem [Python](https://www.python.org/downloads/windows/) (v 3.11).

## Instalação
Primeiramente em um diretório local de preferência faça o clone do repositório:
```shell
cd <path>
git clone https://github.com/Machally/AIcast.git
```
Dentro do repositório local criar um ambiente virtual python, em seguida o ative e realize a instalação das dependências:
```shell
cd AIcast
python -m venv ./.AIcast
.\.AIcast\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## Configuração das APIs
Crie um arquivo .env no repositório local e adicione as API keys
```shell
OPENAI_API_KEY="SuAChaveDaopenAI"
GOOGLE_API_KEY="SuaChaveDoGoogleAIstudio"
```
## Execução
Para executar o programa basta editar a string 'msg' com as orientações iniciais para a IA Gemini e executar o programa AIcast.py
```shell
python AIcast.py
```
