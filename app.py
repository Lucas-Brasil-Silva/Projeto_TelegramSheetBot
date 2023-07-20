from google_sheets_api import GoogleSheets
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
    )
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

ESCOLHER_OPCAO,ENTRADA_PASSO_1,ENTRADA_PASSO_2,ENTRADA_PASSO_3,ENTRADA_PASSO_4,SAIDA_PASSO_1,SAIDA_PASSO_2,SAIDA_PASSO_3,SAIDA_PASSO_4,SAIDA_PASSO_5,SAIDA_PASSO_6,TRANSFERENCIA_PASSO_1,TRANSFERENCIA_PASSO_2,TRANSFERENCIA_PASSO_3,TRANSFERENCIA_PASSO_4,TRANSFERENCIA_PASSO_5,RELATORIO_PASSO_1,RELATORIO_PASSO_2,RELATORIO_PASSO_3 = range(19)

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Entradas','Saídas','Transferência','Relatório']]
    await update.message.reply_text('Escolha uma opção:',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return ESCOLHER_OPCAO

async def tratandoErro(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message(
        '⚠️ Comando não reconhecido. ⚠️\n Clique no quadrado com quatro pontos dentro 🎛️ na parte inferior direita da tela, para visualizar as opções!')

async def entradaPasso1(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Salário','13° Salário','Reembolso','Bônus','Outros']]
    await update.message.reply_text('Qual é a Entrada que deseja registrar?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return ENTRADA_PASSO_1

async def entradaPasso2(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Categoria'] = update.message.text
    await update.effective_chat.send_message(f'⚠️ No caso de valor com vírgula \",\".\n Substitua a vírgula por ponto \".\" ⚠️',reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text('Qual foi o valor da entrada?',reply_markup=ReplyKeyboardRemove())
    return ENTRADA_PASSO_2

async def entradaPasso3(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['valor'] = update.message.text
    keyboard = [['Sim','Não']]
    await update.message.reply_text('Deseja adicionar algum comentário?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return ENTRADA_PASSO_3

async def entradaPasso4(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == 'Sim':
        await update.message.reply_text('Digite o comentário:',reply_markup=ReplyKeyboardRemove())
        return ENTRADA_PASSO_4
    
    else:
        await update.effective_chat.send_message('Prosseguindo sem comentário!',reply_markup=ReplyKeyboardRemove())
        return await finalizarEntrada(update,context)

async def finalizarEntrada(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    google_sheets_api = GoogleSheets()
    categoria = context.user_data['Categoria']
    valor = context.user_data['valor']
    comentario = update.message.text

    try:
        if comentario != 'Não':
            google_sheets_api.inserir_entrada(categoria,valor,comentario)
            await update.effective_chat.send_message('Nova Entrada registrada com sucesso!',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
            
        else:
            comentario =''
            google_sheets_api.inserir_entrada(categoria,valor,comentario)
            await update.effective_chat.send_message('Nova Entrada registrada com sucesso!',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

    except Exception as error:
        print(error)
        await update.effective_chat.send_message('Tente novamente em alguns minutos!',reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

async def saidaPasso1(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Fixa','Variável','Única']]
    await update.message.reply_text('Qual seria a classificação da saída que deseja registrar?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return SAIDA_PASSO_1

async def saidaPasso2(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Contas','Manutenção','Assinaturas','Saúde']]
    context.user_data['Classificação'] = update.message.text
    await update.message.reply_text('Qual a categoria da saída?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return SAIDA_PASSO_2

async def saidaPasso3(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Pix','Cartão de Crédito','Cartão de Debito','Transferência']]
    context.user_data['Categoria'] = update.message.text
    await update.message.reply_text('Qual foi a forma de pagamento?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return SAIDA_PASSO_3

async def saidaPasso4(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Tipo pagamento'] = update.message.text
    await update.effective_chat.send_message(f'⚠️ No caso de valor com vírgula \",\".\n Substitua a vírgula por ponto \".\" ⚠️',reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text('Qual foi o valor da saída?',reply_markup=ReplyKeyboardRemove())
    return SAIDA_PASSO_4

async def saidaPasso5(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['valor'] = update.message.text
    keyboard = [['Sim','Não']]
    await update.message.reply_text('Deseja adicionar algum comentário?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return SAIDA_PASSO_5

async def saidaPasso6(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == 'Sim':
        await update.message.reply_text('Digite o comentário:',reply_markup=ReplyKeyboardRemove())
        return SAIDA_PASSO_6
    
    else:
        await update.effective_chat.send_message('Prosseguindo sem comentário!',reply_markup=ReplyKeyboardRemove())
        return await finalizarSaida(update,context)

async def finalizarSaida(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    google_sheets_api = GoogleSheets()
    classificacao = context.user_data['Classificação']
    categoria = context.user_data['Categoria']
    tipo_pagamento = context.user_data['Tipo pagamento']
    valor = context.user_data['valor']
    comentario = update.message.text

    try:
        if comentario != 'Não':
            google_sheets_api.inserir_saida(classificacao,categoria,tipo_pagamento,valor,comentario)
            await update.effective_chat.send_message('Nova Saída registrada com sucesso!',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        
        else:
            comentario =''
            google_sheets_api.inserir_saida(classificacao,categoria,tipo_pagamento,valor,comentario)
            await update.effective_chat.send_message('Nova Saída registrada com sucesso!',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

    except Exception as error:
        print(error)
        await update.effective_chat.send_message('Tente novamente em alguns minutos!',reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

async def transferenciaPasso1(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Conta 1','Conta 2','Conta 3']]
    await update.message.reply_text('De qual conta você está transferindo?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return TRANSFERENCIA_PASSO_1

async def transferenciaPasso2(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Conta 1','Conta 2','Conta 3']]
    context.user_data['Conta remetente'] = update.message.text
    await update.message.reply_text('Pra qual conta você está transferindo?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return TRANSFERENCIA_PASSO_2

async def transferenciaPasso3(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Conta destino'] = update.message.text
    await update.effective_chat.send_message(f'⚠️ No caso de valor com vírgula \",\".\n Substitua a vírgula por ponto \".\" ⚠️',reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text('Qual o valor da transferência?',reply_markup=ReplyKeyboardRemove())
    return TRANSFERENCIA_PASSO_3

async def transferenciaPasso4(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['valor'] = update.message.text
    keyboard = [['Sim','Não']]
    await update.message.reply_text('Deseja adicionar algum comentário?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return TRANSFERENCIA_PASSO_4

async def transferenciaPasso5(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == 'Sim':
        await update.message.reply_text('Digite o comentário:',reply_markup=ReplyKeyboardRemove())
        return TRANSFERENCIA_PASSO_5
    
    else:
        await update.effective_chat.send_message('Prosseguindo sem comentário!',reply_markup=ReplyKeyboardRemove())
        return await finalizarTransferencia(update,context)

async def finalizarTransferencia(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    google_sheets_api = GoogleSheets()
    conta_remetente = context.user_data['Conta remetente']
    conta_destino = context.user_data['Conta destino']
    valor = context.user_data['valor']
    comentario = update.message.text

    try:
        if comentario != 'Não':
            google_sheets_api.inserir_transferencia(conta_remetente,conta_destino,valor,comentario)
            await update.effective_chat.send_message('Nova Transferêcia registrada com sucesso!',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        
        else:
            comentario = ''
            google_sheets_api.inserir_transferencia(conta_remetente,conta_destino,valor,comentario)
            await update.effective_chat.send_message('Nova Transferêcia registrada com sucesso!',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

    except Exception as error:
        print(error)
        await update.effective_chat.send_message('Tente novamente em alguns minutos!',reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

async def relatorioPasso1(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [['Total Entradas','Total Saídas','Total Transferências']]
    await update.message.reply_text('Qual relatório você deseja visualizar?',reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
    return RELATORIO_PASSO_1

async def relatorioPasso2(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Titulo'] = update.message.text
    await update.message.reply_text('Digite o mes do relatório:',reply_markup=ReplyKeyboardRemove())
    return RELATORIO_PASSO_2

async def relatorioPasso3(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.isdigit():
        context.user_data['Mes'] = update.message.text
        await update.message.reply_text('Digite o ano do relatório: ',reply_markup=ReplyKeyboardRemove())
        return RELATORIO_PASSO_3
    else:
        await update.effective_chat.send_message(f'🔢 Por Favor, Digite somente numeros!',reply_markup=ReplyKeyboardRemove())
        await update.effective_chat.send_message(f'Digite o mes do relatório:',reply_markup=ReplyKeyboardRemove())
        return RELATORIO_PASSO_2

async def relatorioPasso4(update:Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.isdigit():
        context.user_data['Ano'] = update.message.text
        return await relatoriofinal(update,context)

    else:
        await update.effective_chat.send_message(f'🔢 Por Favor, Digite somente numeros!',reply_markup=ReplyKeyboardRemove())
        await update.effective_chat.send_message(f'Digite o ano do relatório: ',reply_markup=ReplyKeyboardRemove())
        return RELATORIO_PASSO_3

async def relatoriofinal(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    google_sheets_api = GoogleSheets()
    titulo = context.user_data['Titulo']
    data = context.user_data['Mes'] + '/' + context.user_data['Ano']

    try:
        if titulo == 'Total Entradas':
            relatorio = google_sheets_api.relatorio_entrada(data)
            await update.effective_chat.send_message(f'Relatório {titulo}: R$ {relatorio}\nCorrespondente a Data: {data}',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        
        elif titulo == 'Total Saídas':
            relatorio = google_sheets_api.relatorio_saida(data)
            await update.effective_chat.send_message(f'Relatório {titulo}: R$ {relatorio}\nCorrespondente a Data: {data}',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        
        elif titulo == 'Total Transferências':
            relatorio = google_sheets_api.relatorio_transferencia(data)
            await update.effective_chat.send_message(f'Relatório {titulo}: R$ {relatorio}\nCorrespondente a Data: {data}',reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
    
    except Exception as error:
        print(error)
        await update.effective_chat.send_message('Tente novamente em alguns minutos!',reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

def main() -> None:
    application = Application.builder().token('TOKEN DO BOT').build()

    conv_handler = ConversationHandler(
        entry_points= [
            CommandHandler('start',start),
            CommandHandler('iniciar',start)
        ],

        states= {            
            ESCOLHER_OPCAO:[
                MessageHandler(filters.Regex('^(Entradas)$'),entradaPasso1),
                MessageHandler(filters.Regex('^(Saídas)$'),saidaPasso1),
                MessageHandler(filters.Regex('^(Transferência)$'),transferenciaPasso1),
                MessageHandler(filters.Regex('^(Relatório)$'),relatorioPasso1),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],

            ENTRADA_PASSO_1:[
                MessageHandler(filters.Regex('^(Salário|13° Salário|Reembolso|Bônus|Outros)$'),entradaPasso2),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            ENTRADA_PASSO_2:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,entradaPasso3)
            ],
            ENTRADA_PASSO_3:[
                MessageHandler(filters.Regex('^(Sim|Não)$'),entradaPasso4),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            ENTRADA_PASSO_4:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,finalizarEntrada)
            ],
            SAIDA_PASSO_1:[
                MessageHandler(filters.Regex('^(Fixa|Variável|Única)$'),saidaPasso2),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            SAIDA_PASSO_2:[
                MessageHandler(filters.Regex('^(Contas|Manutenção|Assinaturas|Saúde)$'),saidaPasso3),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            SAIDA_PASSO_3:[
                MessageHandler(filters.Regex('^(Pix|Cartão de Crédito|Cartão de Debito|Transferência)$'),saidaPasso4),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            SAIDA_PASSO_4:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,saidaPasso5)
            ],
            SAIDA_PASSO_5:[
                MessageHandler(filters.Regex('^(Sim|Não)$'),saidaPasso6),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            SAIDA_PASSO_6:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,finalizarSaida)
            ],
            TRANSFERENCIA_PASSO_1:[
                MessageHandler(filters.Regex('^(Conta 1|Conta 2|Conta 3)$'),transferenciaPasso2),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            TRANSFERENCIA_PASSO_2:[
                MessageHandler(filters.Regex('^(Conta 1|Conta 2|Conta 3)$'),transferenciaPasso3),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            TRANSFERENCIA_PASSO_3:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,transferenciaPasso4)
            ],
            TRANSFERENCIA_PASSO_4:[
                MessageHandler(filters.Regex('^(Sim|Não)$'),transferenciaPasso5),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            TRANSFERENCIA_PASSO_5:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,finalizarTransferencia)
            ],
            RELATORIO_PASSO_1:[
                MessageHandler(filters.Regex('^(Total Entradas|Total Saídas|Total Transferências)$'),relatorioPasso2),
                MessageHandler(filters.TEXT & ~filters.COMMAND,tratandoErro)
            ],
            RELATORIO_PASSO_2:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,relatorioPasso3)
            ],
            RELATORIO_PASSO_3:[
                MessageHandler(filters.TEXT & ~filters.COMMAND,relatorioPasso4)
            ]
        },

        fallbacks= [
            CommandHandler('start',start),
            CommandHandler('iniciar',start)
        ]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
