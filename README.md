# Citizen Assist AI Energia — Global Solution 2026.2 | SERS

**Disciplina:** Soluções em Energias Renováveis e Sustentáveis (SERS) — FIAP, Ciência da Computação, turmas 1CC.  
**Projeto independente de SERS:** a implementação reutiliza a arquitetura do assistente da equipe e concentra-se exclusivamente nas orientações de consumo e sustentabilidade.

## Integrantes

| Integrante | RM |
|---|---|
| David Gabriel | 574147 |
| Enzo Christino | 572047 |
| João Lucas | 571355 |

## Link do vídeo não listado: https://youtu.be/Pe60EgFM2GE

## 1. Público e problema

**Público:** estudantes de Ciência da Computação que usam notebooks para programar, realizar trabalhos e assistir às aulas. **Problema:** como estimar o consumo elétrico de uma estação de estudos e decidir entre economizar energia e adotar uma fonte renovável, considerando custos e impactos ambientais?

A solução é um chatbot Python com respostas baseadas em **três orientações de energia**, fontes verificáveis e números documentados. A busca usa palavras-chave e regras de pontuação, **sem IA generativa**. O estudo é uma **simulação didática**, sem medição de aparelhos nem orçamento real de energia solar.

## 2. Cenário e comparação das alternativas

**Período comum:** um mês; notebook usado **5 h/dia em 22 dias**, sem periféricos. Valores de potência, tarifa, geração e investimento são hipóteses explicitadas em [`analise/premissas.json`](analise/premissas.json).

| Indicador | Rede elétrica: referência | Alternativa A: eficiência | Alternativa B: solar fotovoltaica |
|---|---:|---:|---:|
| Potência média do notebook | 30 W | 20 W (hipótese) | 30 W |
| Consumo do notebook | 3,30 kWh/mês | 2,20 kWh/mês | 3,30 kWh/mês (a demanda não muda) |
| Redução de demanda | — | 1,10 kWh/mês (33,3%) | 0 kWh: muda a fonte/compensação |
| Custo variável **simulado** do notebook | R$ 3,30/mês | R$ 2,20/mês | Até R$ 0 no limite ideal, **não** a fatura real |
| Investimento **hipotético** | R$ 0 | R$ 0 (ajustes existentes) | R$ 5.000 (sistema doméstico 1 kWp) |

**Como calculamos:** `Energia (kWh/mês) = potência (W) × horas/dia × dias/mês ÷ 1.000`. A tarifa **R$ 1,00/kWh é fictícia** e não representa conta de luz real. A potência média 30 W foi escolhida dentro de uma faixa pública de **10–38 W** para notebooks [1]; a redução para 20 W é uma hipótese **não medida**.

A fonte renovável é um **sistema solar fotovoltaico conectado à rede, hipotético, de 1 kWp**. Com 4 h/dia de sol pleno equivalentes, 30 dias e fator 0,80, a geração total teórica seria **96 kWh/mês para o sistema inteiro**, dos quais **no máximo 3,30 kWh** podem ser atribuídos à demanda deste notebook. O sistema **não** foi dimensionado economicamente para a residência e não garante conta zerada. A compensação depende das regras da ANEEL [2].

**Comparação de viabilidade:** ajustar configurações de energia é mais justificável para **um notebook isolado**. Comprar 1 kWp apenas para essa carga seria desproporcional: ao atribuir todo o investimento fictício aos até R$ 3,30 mensais de economia do notebook, o retorno didático ideal ultrapassa **126 anos**; **não** é previsão de retorno para um imóvel com outros consumos.

**Impacto ambiental:** a eficiência reduz demanda (se a hipótese for atingida), sem acrescentar equipamentos. A geração solar usa fonte renovável, mas tem impactos de produção e destinação dos componentes, não quantificados aqui. Não calculamos CO2 evitado. O resultado depende de insolação, sombras, perdas, uso e fatura real.

**Recomendação:** priorizar configurações de economia, brilho e suspensão sem atrapalhar os estudos; considerar energia solar apenas após analisar o **consumo de toda a residência**, a irradiação do local, custos e compensação.

➡️ **Análise completa com contas, justificativas e limitações:** [`analise/analise_energetica.md`](analise/analise_energetica.md).  
➡️ **Cálculos reproduzíveis:** [`analise/calcular.py`](analise/calcular.py), [`analise/premissas.json`](analise/premissas.json) e [`analise/comparacao.csv`](analise/comparacao.csv).

## 3. Funcionalidades no Citizen Assist AI Energia

A base [`data/base_conhecimento.json`](data/base_conhecimento.json) contém três orientações na categoria **Energia e sustentabilidade**:

1. Estimar o consumo e o custo mensal de um notebook.
2. Economizar eletricidade durante os estudos.
3. Comparar energia solar fotovoltaica e eficiência para a mesma necessidade.

**Perguntas de demonstração:** `Quanto gasta meu notebook de energia?`, `Como economizar energia no notebook?` e `Vale a pena energia solar para notebook?`.

O assistente mostra resposta, números da análise, fonte e data. O histórico de atendimentos (`data/historico.json`) e a exportação (`data/atendimentos.csv`) **são criados durante a utilização**, não contêm testes fictícios no projeto inicial. As evidências e comentários reais devem ser documentados em [`testes/registro_testes.md`](testes/registro_testes.md).

## 4. Como executar (sem dependências externas)

Tenha **Python 3** instalado e abra o terminal na **raiz deste repositório**.

**Interface web:**

```bash
python3 web_app.py
```

Depois abra `http://127.0.0.1:8000/` ou diretamente `http://127.0.0.1:8000/usuario`. A área `http://127.0.0.1:8000/operador` mostra os indicadores de testes da **SERS**, separados das consultas feitas pelo operador. Use `Ctrl+C` para encerrar o servidor. Se a porta estiver ocupada, use `python3 web_app.py --porta 8001`.

**Terminal (alternativo):**

```bash
python3 main.py
```

**Recalcular e gerar as tabelas:**

```bash
python3 analise/calcular.py
```

Os cálculos usam somente a biblioteca padrão do Python. **O HTML sozinho não funciona sem o servidor Python.**

## 5. Organização do repositório

```text
README.md
main.py
orientacao.py
base_conhecimento.py
assistente.py
web_app.py
web/index.html
data/base_conhecimento.json
analise/premissas.json
analise/calcular.py
analise/comparacao.csv
analise/analise_energetica.md
testes/registro_testes.md
```

**Observação:** `data/historico.json` e `data/atendimentos.csv` são gerados automaticamente depois das interações com o chatbot. Não há relatórios inventados nem documentos administrativos no repositório.

## 6. Testes com usuários e ajustes

O enunciado exige verificar compreensão e utilidade das orientações, **registrar situações, comentários e ajustes**, sem dados pessoais desnecessários, mas não estabelece quantidade mínima de participantes. Os registros específicos da disciplina devem ser inseridos em [`testes/registro_testes.md`](testes/registro_testes.md), junto de comentários reais e de eventuais alterações comprovadas. O painel registra útil/não útil e nota de facilidade; o registro manual documenta a **compreensão e os comentários**. Antes da entrega, preencha o registro com os resultados específicos das orientações de energia; não utilize resultados de outro estudo.

## 7. Decisão técnica e limitações

- **Arquitetura:** reaproveitamento independente do Citizen Assist AI feito pela equipe; três classes (`Orientacao`, `BaseConhecimento`, `Assistente`) com base JSON, cálculo separado e interface local. A base e os dados usados aqui são específicos do cenário de energia.
- **Correspondência:** a busca é por palavras-chave e pode não compreender todas as formas de perguntar; a confiança representa correspondência textual, não precisão científica.
- **Estimativas:** potência, redução de consumo, tarifa, investimento e geração solar são hipóteses. Os valores não são medições, cotações ou promessa de economia.
- **Localidade:** cálculo solar não utiliza coordenadas reais, sombras nem histórico meteorológico local; para projeto de instalação, consulte CRESESB/PVGIS e especialistas.
- **Privacidade:** a interface gera IDs anônimos para as sessões; evite inserir dados pessoais. O painel do operador não possui autenticação; use **apenas localmente**.

## 8. Fontes e vídeo

[1] Governo da Austrália (SA), potência típica de notebooks: https://www.sa.gov.au/topics/energy-and-environment/using-saving-energy/using-and-buying-appliances/electronics  
[2] ANEEL, micro e minigeração distribuída e compensação: https://www.gov.br/aneel/pt-br/assuntos/geracao/geracao-distribuida  
[3] Departamento de Energia dos EUA, computadores eficientes: https://www.energy.gov/cmei/femp/purchasing-energy-efficient-computers  
[4] CRESESB, SunData: https://www.cresesb.cepel.br/index.php?section=sundata  
[5] JRC/Comissão Europeia, PVGIS: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis_en  
[6] EPE, fontes de geração: https://www.epe.gov.br/pt/areas-de-atuacao/energia-eletrica/expansao-da-geracao/fontes
