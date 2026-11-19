# Análise energética — Citizen Assist AI Energia (SERS)

**Disciplina:** Soluções em Energias Renováveis e Sustentáveis — FIAP, Global Solution 2026.2  
**Equipe:** David Gabriel (RM 574147), Enzo Christino (RM 572047), João Lucas (RM 571355)  
**Data de preparação:** 19/11/2026  
**Natureza dos dados:** estudo didático com hipóteses explicitadas. Não houve medição elétrica, orçamento profissional nem cálculo solar com coordenadas reais.

## 1. Público, problema e proposta

O público é formado por estudantes de Ciência da Computação que usam notebooks para programar, assistir a aulas e pesquisar. A necessidade é atender **5 horas diárias de estudo em 22 dias do mês** com a menor despesa e impacto ambiental razoável.

Pergunta central: **vale mais a pena economizar energia no notebook ou instalar geração solar para atendê-lo?**

A análise fundamenta as três orientações do Citizen Assist AI Energia, numa versão independente para SERS, na categoria **Energia e sustentabilidade** (IDs 1, 2 e 3). O assistente mostra valores, fontes e limitações sem IA generativa.

## 2. Premissas, unidades, origem e período

| Parâmetro | Hipótese de trabalho | Status e origem |
|---|---|---|
| Equipamento | notebook genérico | cenário delimitado; não existe aparelho medido |
| Potência média de referência | **30 W** | hipótese escolhida dentro de 10–38 W, faixa orientativa de notebooks publicada pelo governo da Austrália [1] |
| Potência no modo eficiente | **20 W** | hipótese ilustrativa para comparar, dentro da mesma faixa [1]; não representa redução garantida |
| Tempo de estudo | **5 h por dia × 22 dias por mês** | rotina hipotética de estudante, adotada pela equipe |
| Tarifa marginal simplificada | **R$ 1,00/kWh** | parâmetro hipotético; não equivale à tarifa oficial nem inclui encargos |
| Investimento em ajuste de energia | **R$ 0** | hipótese: uso apenas de configurações já disponíveis |
| Solar fotovoltaica | **1,0 kWp** | instalação doméstica hipotética, maior que a carga estudada |
| Sol pleno equivalente | **4,0 h/dia** | valor hipotético, não média medida ou consultada para endereço de São Paulo; metodologia de irradiação: CRESESB [3] e PVGIS [4] |
| Fator global de desempenho PV | **0,80** | hipótese de 20% de perdas agregadas; depende de local, orientação e equipamento [4] |
| Geração solar | **30 dias no mês** | mês simplificado; insolação não se limita aos 22 dias de estudo |
| Investimento solar | **R$ 5.000** | hipótese numérica, **não é orçamento/cotação nem preço verificado de mercado** |

**Potência do carregador não é potência consumida:** usar o valor nominal do adaptador como média de operação seria incorreto. A estimativa envolve energia na tomada; fatores como recarga da bateria e periféricos não foram medidos.

## 3. Cálculos de consumo para o mesmo notebook

Fórmula usada em todas as alternativas: `Energia (kWh/mês) = potência média (W) × horas por dia (h) × dias no mês / 1000`.

**Sem intervenção / referência:**

`30 W × 5 h/dia × 22 dias ÷ 1000 = 3,30 kWh/mês`.

Custo variável *somente teórico*, com tarifa fictícia: `3,30 × R$ 1,00 = R$ 3,30/mês`.

**Alternativa A — eficiência energética:**

Hipótese de adotar configurações de economia, suspender o aparelho em inatividade e reduzir o brilho de maneira que a potência média passe de 30 W para 20 W. A passagem é **simulada**, não medida nem assegurada.

`20 W × 5 × 22 ÷ 1000 = 2,20 kWh/mês`.

Redução hipotética: `3,30 − 2,20 = 1,10 kWh/mês` = **33,3%** do consumo de referência. Redução máxima do custo variável simulado: **R$ 1,10/mês**, ou **R$ 13,20 em 12 meses**, sem investimento adicional suposto.

**Alternativa B — energia solar fotovoltaica (fonte renovável):**

Cálculo ilustrativo de geração: `potência PV (kWp) × sol pleno equivalente (h/dia) × dias × fator de desempenho`.

`1,0 kWp × 4,0 h/dia × 30 dias × 0,80 = 96,0 kWh/mês` de produção **hipotética para o sistema inteiro**. Não é geração medida nem cálculo geográfico baseado no endereço.

Para uma comparação honesta, a **parcela de consumo do notebook continua sendo só 3,30 kWh/mês**. Não podemos atribuir os 96 kWh inteiros ao notebook. Neste cenário idealizado, no máximo 3,30 kWh/mês da geração poderiam atender/compensar a demanda do notebook; eventual excedente dependeria de outros equipamentos e regras da rede.

Redução **máxima puramente ilustrativa** do custo variável atribuível ao notebook: `3,30 kWh × R$ 1,00/kWh = R$ 3,30/mês`. O valor realmente faturado pode ser maior devido às condições e componentes tarifários e ao sistema de compensação regulamentado pela ANEEL [5]. Uma instalação isolada com bateria precisaria de outra análise; este exemplo supõe sistema conectado à rede, sem garantia de uso direto à noite.

Com custo de instalação **hipotético** de R$ 5.000, o retorno mais otimista, atribuindo economia somente ao notebook, seria `R$ 5.000 ÷ R$ 3,30/mês ≈ 1515,15 meses ≈ 126,26 anos`. Este número é um **limite didático de baixa viabilidade**, e não um estudo de investimento: não inclui manutenção, financiamento, desgaste, impostos, custo de disponibilidade ou possível compensação do restante da casa. Não é correto aplicar o payback de um sistema residencial inteiro sem analisar a residência.

## 4. Comparação no mesmo mês e na mesma necessidade

| Situação | Consumo do notebook | Geração solar teórica do sistema | Custo variável teórico atribuído ao notebook | Investimento simulado | Observação |
|---|---:|---:|---:|---:|---|
| Rede elétrica — referência | 3,30 kWh | 0 | R$ 3,30/mês | R$ 0 | sem mudança de hábito |
| A. Eficiência energética | 2,20 kWh | 0 | R$ 2,20/mês | R$ 0 | economiza 1,10 kWh/mês **se** a potência média de 20 W for alcançada |
| B. Solar fotovoltaica | 3,30 kWh | 96,0 kWh/mês para o **sistema inteiro** | **de R$ 0 no limite ideal**, não valor da conta real | R$ 5.000 | até 3,30 kWh do sistema poderiam compensar a carga; custos fixos não incluídos |

Todas as opções atendem às mesmas 5 horas diárias de estudo, 22 dias por mês. Energia solar não reduz fisicamente a potência do notebook, apenas altera a fonte/compensação da energia utilizada. A eficiência diminui a demanda.

## 5. Viabilidade e impactos ambientais

### A. Eficiência energética

- **Custo e implantação:** hipótese de custo inicial zero por usar configurações existentes; nenhuma compra de equipamento.
- **Viabilidade:** é a alternativa recomendada **para um notebook isolado**, condicionada à verificação de que os modos de economia não atrapalham programação e videoaulas.
- **Impacto ambiental:** potencial redução de consumo elétrico em 1,10 kWh/mês (se a hipótese de potência for atingida), sem fabricação de novo sistema; não foi calculada emissão evitada de CO2.
- **Limitações:** a economia real depende de atividade, bateria, brilho, CPU, periféricos e modo ocioso [2].

### B. Solar fotovoltaica

- **Custo e implantação:** alto custo inicial relativo à demanda de 3,30 kWh/mês neste exemplo; exigiria viabilidade de espaço, orientação, inversor, conexão e orçamento real.
- **Viabilidade:** **não recomendamos instalar 1 kWp só para alimentar um notebook**, pois a geração solar simulada é muito maior do que essa carga. Em uma casa com outros consumos, o cenário pode mudar completamente e deve ser refeito.
- **Impacto ambiental:** eletricidade solar não utiliza combustível durante a geração e pode reduzir o consumo atribuído a outras fontes; há impactos de fabricação, materiais e destinação de equipamentos, que não foram quantificados [6].
- **Limitações:** o desempenho varia com insolação, sombras, orientação, perdas, tempo, tarifa e regulamentação [3][4][5]. Não há promessa de conta zerada; a ANEEL indica custo de disponibilidade e demais regras [5].

## 6. Recomendação final ao estudante

**Primeiro, ajustar configurações e hábitos para reduzir consumo**, medindo a diferença quando possível. Se a residência já possui ou deseja instalar geração solar para vários equipamentos, avaliar o sistema usando **a conta residencial inteira e a irradiação do local**; não comprar um sistema solar apenas por causa deste notebook.

A recomendação é **condicional às hipóteses** de potência, rotina, tarifa e instalação. O assistente apresenta esse aviso e fornece fontes para conferência.

## 7. Como os resultados foram integrados ao chatbot

O arquivo `data/base_conhecimento.json` contém a categoria `Energia e sustentabilidade`:

- **ID 1:** consumo e custo do notebook, com os valores **3,30 kWh** e **R$ 3,30/mês simulados**.
- **ID 2:** economia de energia, com **2,20 kWh**, **1,10 kWh poupados** e **33,3%** de redução condicional.
- **ID 3:** alternativa solar, **96,0 kWh/mês para o sistema inteiro**, comparação com **3,30 kWh do notebook**, investimento e viabilidade.

A interface web e o terminal reutilizam a arquitetura Python do Citizen Assist AI, em uma cópia independente para a disciplina de SERS. Basta iniciar `python3 web_app.py` ou `python3 main.py`. O menu de categorias passa a exibir a nova categoria, sem bibliotecas extras.

**Perguntas de demonstração:** `Quanto gasta meu notebook de energia?`; `Como economizar energia no notebook?`; `Vale a pena energia solar para notebook?`.

## 8. Testes com usuários — PENDENTE DE EXECUÇÃO REAL

O enunciado de SERS exige testar compreensão/utilidade, registrar situações, comentários e ajustes realizados. Não especifica quantidade mínima de pessoas para esta disciplina.

O arquivo `testes/registro_testes.md` traz roteiro de três situações e campos para preencher. **Ainda não foram registrados testes reais das orientações de energia neste repositório; não declare que foram realizados.** Testes realizados em outra disciplina não substituem a validação específica das respostas energéticas.

## 9. Referências verificáveis

[1] SA Government (Austrália), eletrônicos e potência típica de notebooks (10–38 W): https://www.sa.gov.au/topics/energy-and-environment/using-saving-energy/using-and-buying-appliances/electronics  
[2] U.S. Department of Energy, utilização eficiente e power management de computadores: https://www.energy.gov/cmei/femp/purchasing-energy-efficient-computers  
[3] CRESESB, SunData, estimativas de irradiação em território nacional: https://www.cresesb.cepel.br/index.php?section=sundata  
[4] Joint Research Centre / Comissão Europeia, PVGIS, energia fotovoltaica e perdas: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis_en  
[5] ANEEL, microgeração/minigeração distribuída, compensação e custos de disponibilidade: https://www.gov.br/aneel/pt-br/assuntos/geracao/geracao-distribuida  
[6] EPE, fontes de geração e impactos da energia solar: https://www.epe.gov.br/pt/areas-de-atuacao/energia-eletrica/expansao-da-geracao/fontes

**Separação de fontes e hipóteses:** [1] respalda uma *faixa de potência*, não os consumos exatos de um equipamento. [3][4] explicam *metodologia e consulta*, mas não foram usados para extrair um dado real do endereço. Os valores de sol, tarifa, investimento e eficiência são *parâmetros definidos para exemplificar um cenário*, e não medidas oficiais ou de mercado.

## 10. Reproduzir os cálculos

Na pasta do projeto, execute:

```bash
python3 analise/calcular.py
```

O script lê `analise/premissas.json` e atualiza `analise/comparacao.csv`. Não é necessário instalar bibliotecas. Para demonstrar na avaliação, mostre a planilha CSV ou o relatório e uma resposta coerente do chatbot.
