#pip install pyinstaller
# Diretório ants de "app"
# pyinstaller --onefile --add-data "app/view/index.html;view" --add-data "app/view/css;view/css" --add-data "app/view/js;view/js" --add-data "app/model/armazenamento;armazenamento" --hidden-import "pandas._libs.tslibs.timedeltas" --hidden-import "pandas._libs.tslibs.timestamps" --hidden-import "pandas._libs.tslibs.np_datetime" --hidden-import "pandas._libs.tslibs.nattype" --hidden-import "pandas._libs.tslibs.timezones" app/model/Server.py
# cd dist
# .\Server.exe 
from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import io
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

app = Flask(__name__, static_folder=resource_path('view'), template_folder=resource_path('view'))

#Define ordm coluns desejad
colunas_ordem = ["Data Req.", "Requisição", "Requisitante", "Veículo/Equip.", "Km Percorrido", "Km por Litro", "Litros Restantes", "Km Atual", "Km Rodados", "Litros Abastecidos", "Litros", "Vlr. Total", "Obs."]

def process_excel(file):
    df = pd.read_excel(file, engine='openpyxl')
    df['Data Req.'] = pd.to_datetime(df['Data Req.'], errors='coerce', dayfirst=True)
    df = df.sort_values(by=['Veículo/Equip.', 'Data Req.'])
    df['Km Percorrido'] = df.groupby('Veículo/Equip.')['Km Atual'].diff().abs()
    df['Litros Abastecidos'] = df.groupby('Veículo/Equip.')['Litros'].shift(1)
    df['Km por Litro'] = df['Km Percorrido'] / df['Litros Abastecidos']
    df['Km por Litro'] = df['Km por Litro'].round(3)
    df['Litros Restantes'] = df['Litros'] - df['Km por Litro']
    
    #Reorden coluns follwing list'colunas_ordem'
    df = df[colunas_ordem]
    
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'})
    file = request.files['file']
    global df_processed
    df_processed = process_excel(file)
    processed_data_path = os.path.join(app.root_path, 'armazenamento', "processed_data.xlsx")
    df_processed.to_excel(processed_data_path, index=False)
    return jsonify({'message': 'Arquivo processado com sucesso', 'download_url': '/download'})

@app.route('/filter', methods=['POST'])
def filter_data():
    filters = request.json
    df_filtered = df_processed.copy()

    if filters.get('VeiculoEquip'):
        df_filtered = df_filtered[df_filtered['Veículo/Equip.'] == filters['VeiculoEquip']]
    
    if filters.get('DataInicial'):
        df_filtered = df_filtered[df_filtered['Data Req.'] >= pd.to_datetime(filters['DataInicial'], dayfirst=True)]
    
    if filters.get('DataFinal'):
        df_filtered = df_filtered[df_filtered['Data Req.'] <= pd.to_datetime(filters['DataFinal'], dayfirst=True)]
    
    #Reorden coluns accordng t/t-list'colunas_ordem'
    df_filtered = df_filtered[colunas_ordem]
    
    filtered_data_path = os.path.join(app.root_path, 'armazenamento', "filtered_data.xlsx")
    df_filtered.to_excel(filtered_data_path, index=False)
    return jsonify({'message': 'Dados filtrados com sucesso', 'download_url': '/download_filtered'})

@app.route('/download')
def download_file():
    processed_data_path = os.path.join(app.root_path, 'armazenamento', "processed_data.xlsx")
    return send_file(processed_data_path, as_attachment=True)

@app.route('/download_filtered')
def download_filtered():
    filtered_data_path = os.path.join(app.root_path, 'armazenamento', "filtered_data.xlsx")
    return send_file(filtered_data_path, as_attachment=True)

@app.route('/clean_and_exit', methods=['POST'])
def clean_and_exit():
    #Clear arqvs from'armazenamento'
    storage_path = os.path.join(app.root_path, 'armazenamento')
    for filename in os.listdir(storage_path):
        file_path = os.path.join(storage_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Erro ao apagar {file_path}: {e}')
    
    #Kill server
    os._exit(0)
    return jsonify({'message': 'Limpeza completa e servidor finalizado'})

if __name__ == '__main__':
    if not os.path.exists(resource_path('armazenamento')):
        os.makedirs(resource_path('armazenamento'))
    app.run(debug=True, port=5003)