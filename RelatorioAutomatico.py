#Instalar Bibliotecas (pywin32, pandas,pymssql,openpyxl,cx_Freeze)

import win32com.client as wind32
import pandas as pd
import pymssql as sql
import time as tempo

print('Processo de Leitura, gravação e envio de e-mail dos clientes inativos!')
print('')
print('Iniciando...')

tempo.sleep(2)
sqlTEXT = ""
sqlEXEC = '''   SELECT max(e090rep.nomrep) as NomRep,                                                                   \
                       max(e085cli.nomcli) as Cliente,                                                                   \
                       max(e085cli.tipcli)as Tipo_Cliente,                                                              \
                       max(e085cli.tipmer) as Mercado,                                                                  \
                       max(e085cli.cgccpf) as CNPJ,                                                                     \
                       max(e085cli.codcli) as Cod_Cliente,                                                              \
                       max(e085cli.endcli) as Endereço,                                                                 \
                       max(e085cli.baicli) as Bairro,                                                                   \
                       max(e085cli.cidcli) as Cidade,                                                                   \
                       max(e085cli.sigufs) as Estado,                                                                   \
                       max(e085cli.foncli) as Telefone,                                                                 \
                       max(e085cli.foncl2) as Telefone2,                                                                \
                       max(e085cli.foncl3) as Telefone3,                                                                 \
                       max(e085cli.intnet) as Email,                                                                    \
                       max(e120ped.codrep) as codrep,                                                                   \
                       max(e120ped.datemi) as datemi,                                                                   \
                       max(e085hcl.datufa) as UltFat,                                                                   \
                       max(e085hcl.vlrufa) as ValFat                                                                    \
                  FROM e085cli, e120ped, e090rep,e085hcl                                                                \
                 WHERE e085cli.codcli NOT IN (SELECT codcli                                                             \
                                                FROM e120ped                                                            \
                                               WHERE e085cli.codcli = e120ped.codcli                                    \
                                                 AND e120ped.datemi >= convert (date, getdate()-95) )                   \
                   AND e085cli.codcli=e120ped.codcli                                                                    \
                   AND e085cli.tipmer = ('I')                                                                           \
                   AND e085cli.tipcli = ('J')                                                                           \
                   AND e085cli.tipemp not in ('8')                                                                      \
                   AND e085cli.codgre not in ('82','187')                                                               \
                   AND e085cli.confin not in ('S')                                                                      \
                   AND e085cli.clifor not in ('F','A')                                                                  \
                   AND e085cli.codrtr not in ('1')                                                                      \
                   AND e085hcl.codcli = e085cli.codcli                                                                  \
                   AND e090rep.codrep = e120ped.codrep                                                                  \
                   AND e085cli.usu_bloven = ('N')                                                                       \
                   AND e085hcl.confin not in ('S')                                                                      \
                   AND e085hcl.vlrufa > 0                                                                               \
                   AND e085cli.codcli not in (1,2,3,4,5,6)                                                               \
              GROUP BY e085cli.codcli '''

conexao = sql.connect('192.168.1.239','sapiens','sapiens','sapiens')
dataSQL = pd.read_sql_query(sqlEXEC,conexao)
dados = pd.DataFrame(dataSQL)
conexao.close()

#grava dados excel
dados.to_excel('dados.xlsx', index = False)
tempo.sleep(3)
CliIna = len(dados)
print('')
print('Dados Lidos e salvos em Excel')

print('Total de Clientes: ', CliIna)

tempo.sleep(10)

"""enviar e-mail Automático"""
#criar integração do outlook
outlook = wind32.Dispatch('outlook.application')
#criar e-mail
email = outlook.CreateItem(0)
#Configurar anexo
anexo = "C:/ProgramasTI/RelatorioAutomatico/RelatorioAutomatico/dados.xlsx"

#configurar as informações do seu e-mail
#listaemail = "ti@clarice.com.br;luana.mayer@clarice.com.br;everton.galiazzi@clarice.com.br;francinara.pereira@clarice.com.br;henrique.lanzarini@clarice.com.br;bruno.morales@clarice.com.br"
listaemail = "ti@clarice.com.br"
email.To = listaemail  #destinatário
email.Subject = "Relatório de Clientes inativos"     #Titulo
email.Attachments.Add(anexo)                         #Anexo

email.HTMLBody = f"""
<p>Bom dia! </p>
<p>Segue lista de clientes que não tiveram pedidos efetuados em 90 dias.</p>

<p><strong>Total de Clientes Inativos: {CliIna} </strong></p>

<p>Att. Wilian Carvalho <br />
Departamento de T.I </p>
"""
email.Send()
print('')
print('')
print('E-mail enviado com suscesso.')

tempo.sleep(4)
print('Processo Finalizado.')
print('Obrigado!')
tempo.sleep(3)



