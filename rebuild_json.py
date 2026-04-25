import json

# Estrutura correta: 5 tópicos principais com poucos subtópicos cada
data = {
  "title": "Método Price Action - Oliver Velez",
  "topics": [
    {
      "title": "1. CONHECIMENTOS BÁSICOS",
      "subtopics": [
        {
          "title": "Bolsa de Valores",
          "content": "BOLSA DE VALORES\n\nBM&F - Bolsa de Mercadorias e Futuro\nNegociação de commodities (café, milho, etc) e contratos futuros (índice, dólar, etc.)\n\nB3 - Brasil, Bolsa, Balcão\nIPO - Capital Aberto com negociação de ações (ITUB4, BBDC4, etc.)"
        },
        {
          "title": "Tipos de Traders",
          "content": "TIPOS DE TRADERS\n\nDay Trade\nNegociações abertas e fechadas no mesmo dia. Grande vantagem: alavancagem.\n\nSwing Trade\nNegociações encerradas após dias ou semanas após a entrada.\n\nPosition Trade\nNegociações mantidas por meses ou anos."
        },
        {
          "title": "Corretora de Valores",
          "content": "CORRETORA DE VALORES\n\nInstitução autorizada pela CVM para operar no mercado de capitais.\n\nFunções principais:\n- Executar ordens de compra e venda\n- Análise de ativos\n- Gestão de carteira\n- Consultoria de investimentos\n\nExemplos: XP Investimentos, BTG Pactual, Itaú, Santander"
        }
      ]
    },
    {
      "title": "2. INTRODUÇÃO AO MÉTODO",
      "subtopics": [
        {
          "title": "Análise dos Candles",
          "content": "ANÁLISE DOS CANDLES\n\nOs candles (velas) representam o movimento de preço em um período.\n\nCOMPONENTES:\n- Corpo: diferença entre abertura e fechamento\n- Mechas: máxima e mínima do período\n\nTIPOS:\n- Candle de Alta (corpo verde/branco): fechamento > abertura\n- Candle de Baixa (corpo vermelho/preto): fechamento < abertura"
        },
        {
          "title": "Lei da Continuidade",
          "content": "LEI DA CONTINUIDADE\n\nPrincípio fundamental do Price Action:\n\nUm movimento que não completa um padrão tende a continuar na mesma direção.\n\nAPLICAÇÃO:\nQuando um candle não fecha acima/abaixo do candle anterior de forma definitiva, espera-se que o movimento continue."
        },
        {
          "title": "Tempos Gráficos",
          "content": "TEMPOS GRÁFICOS ANALÍTICOS\n\nM1 - 1 minuto: Scalping, operações muito rápidas\n\nM5 - 5 minutos: Day Trade de curta duração\n\nM15 - 15 minutos: Day Trade padrão\n\nH1 - 1 hora: Swing Trade\n\nD1 - 1 dia: Position Trade, análise de longo prazo"
        }
      ]
    },
    {
      "title": "3. PADRÕES OPERACIONAIS",
      "subtopics": [
        {
          "title": "Setups à Favor da Tendência",
          "content": "SETUPS À FAVOR DA TENDÊNCIA\n\nOperações no sentido do movimento principal do mercado.\n\nVANTAGENS:\n- Maior taxa de acerto\n- Melhor relação risco/retorno\n- Mais previsível\n\nEXEMPLO:\nEm tendência de alta, entrar nas retrações de compra."
        },
        {
          "title": "Setups Contra a Tendência",
          "content": "SETUPS CONTRA A TENDÊNCIA\n\nOperações fazendo o oposto do movimento principal.\n\nRISCOS:\n- Taxa de acerto menor\n- Requer mais precisão\n- Perdas maiores se errar\n\nAPLICAÇÃO:\nSomente com confirmações fortes e gerenciamento rigoroso."
        },
        {
          "title": "Lei dos 2/3",
          "content": "LEI DOS 2/3 (Regra de Proporção)\n\nEm um movimento de reversão ou parada:\nO preço deve recuar 2/3 do movimento anterior para confirmar uma inversão de tendência.\n\nEXEMPLO:\nSe o preço sobe 300 pontos, espera-se uma retração de ~200 pontos (2/3) antes de nova alta."
        }
      ]
    },
    {
      "title": "4. INDICADORES E FERRAMENTAS",
      "subtopics": [
        {
          "title": "Média Móvel",
          "content": "MÉDIA MÓVEL\n\nIndicador que suaviza o preço mostrando a direção da tendência.\n\nTIPOS:\n- Simples (SMA): média aritmética dos preços\n- Exponencial (EMA): dá maior peso aos preços recentes\n\nUSO:\n- MA 20: tendência de curto prazo\n- MA 50: tendência média\n- MA 200: tendência de longo prazo"
        },
        {
          "title": "MACD (Moving Average Convergence Divergence)",
          "content": "MACD\n\nIndicador de momentum que mostra força do movimento.\n\nCOMPONENTES:\n- Linha MACD (rápida)\n- Linha de Sinal (lenta)\n- Histograma (diferença)\n\nSINAIS:\n- Cruzamento acima da linha zero = compra\n- Cruzamento abaixo da linha zero = venda"
        },
        {
          "title": "Volume",
          "content": "ANÁLISE DE VOLUME\n\nVolume indica a força de um movimento.\n\nINTERPRETAÇÃO:\n- Volume ALTO: movimento forte e confiável\n- Volume BAIXO: movimento fraco, pode reverter\n\nREGRA:\nUm movimento deve ser confirmado por volume para ter credibilidade."
        }
      ]
    },
    {
      "title": "5. GESTÃO DE RISCO",
      "subtopics": [
        {
          "title": "Posicionamento (Position Sizing)",
          "content": "POSICIONAMENTO\n\nDefinição do tamanho ideal da posição baseado no risco.\n\nFÓRMULA:\nTamanho da Posição = (Risco em R$) / (Pontos de Stop)\n\nEXEMPLO:\nSe você quer perder no máximo R$ 100 com stop de 50 pontos:\nPosição = 100 / 50 = 2 contratos"
        },
        {
          "title": "Stop Loss",
          "content": "STOP LOSS\n\nNível onde você limita a perda máxima.\n\nCOMO DEFINIR:\n- Técnico: abaixo de suporte/acima de resistência\n- Porcentagem fixa: 2% do capital por operação\n- Volatilidade: baseado no ATR (Average True Range)\n\nRURA OURO:\nNunca operar sem stop loss definido."
        },
        {
          "title": "Relação Risco/Retorno",
          "content": "RELAÇÃO RISCO/RETORNO\n\nMede a qualidade de uma operação.\n\nEXEMPLO:\nRisco: -100 pontos (perda)\nRetorno: +200 pontos (ganho)\nRelação: 1:2 (para cada 1 perdido, ganha 2)\n\nOBJETIVO:\nManter relações mínimas de 1:2 em operações."
        }
      ]
    }
  ]
}

with open('apostila_scraped/landing-page-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK - JSON reconstruido com conteudo organizado!")
