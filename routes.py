from flask import Blueprint, jsonify, request
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/data', methods=['GET'])
def get_data():
    try:
        df = pd.read_csv('data/team_name1_price_fcst.csv')
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/filtered_data', methods=['POST'])
def get_filtered_data():
    try:
        filters = request.get_json()
        df = pd.read_csv('data/team_name1_price_fcst.csv')
        
        if 'date_range' in filters:
            start_date, end_date = filters['date_range']
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        if 'series' in filters:
            series = filters['series']
            if not isinstance(series, list):
                series = [series]
            df = df[df['series'].isin(series)]
        
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/statistics', methods=['POST'])
def calculate_statistics():
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        
        if 'actual_price' in df.columns:
            grouped = df.groupby('date')
            rmse_results = {}

            for name, group in grouped:
                rmse = ((group['actual_price'] - group['price_fcst']) ** 2).mean() ** 0.5
                rmse_results[name] = rmse
            
            return jsonify(rmse_results)
        else:
            return jsonify({"error": "The provided data does not include 'actual_price' column."})
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/filtered_statistics', methods=['POST'])
def calculate_filtered_statistics():
    try:
        filters = request.get_json()
        df = pd.read_csv('data/team_name1_price_fcst.csv')
        
        if 'date_range' in filters:
            start_date, end_date = filters['date_range']
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        if 'series' in filters:
            series = filters['series']
            if not isinstance(series, list):
                series = [series]
            df = df[df['series'].isin(series)]
        
        if 'actual_price' in df.columns:
            grouped = df.groupby('date')
            rmse_results = {}

            for name, group in grouped:
                rmse = ((group['actual_price'] - group['price_fcst']) ** 2).mean() ** 0.5
                rmse_results[name] = rmse
            
            return jsonify(rmse_results)
        else:
            return jsonify({"error": "The filtered data does not include 'actual_price' column."})
    except Exception as e:
        return jsonify({"error": str(e)})
