from flask import Blueprint, jsonify, request, send_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

main = Blueprint('main', __name__)

@main.route('/data', methods=['GET'])
def get_data():
    try:
        df = pd.read_csv('data/team_name1_price_fcst_with_actual.csv')
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/filtered_data', methods=['POST'])
def get_filtered_data():
    try:
        filters = request.get_json()
        df = pd.read_csv('data/team_name1_price_fcst_with_actual.csv')
        
        # Ensure date is treated as string
        df['date'] = df['date'].astype(str)
        
        if 'date_range' in filters:
            start_date, end_date = filters['date_range']
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/filtered_statistics', methods=['POST'])
def calculate_filtered_statistics():
    try:
        filters = request.get_json()
        df = pd.read_csv('data/team_name1_price_fcst_with_actual.csv')
        
        # Ensure date is treated as string
        df['date'] = df['date'].astype(str)
        
        if 'date_range' in filters:
            start_date, end_date = filters['date_range']
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
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

@main.route('/graph', methods=['POST'])
def generate_graph():
    try:
        filters = request.get_json()
        df = pd.read_csv('data/team_name1_price_fcst_with_actual.csv')
        
        # Ensure date is treated as string
        df['date'] = df['date'].astype(str)
        
        if 'date_range' in filters:
            start_date, end_date = filters['date_range']
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        # Data series selection
        if 'series' in filters:
            selected_series = ['date', 'time'] + filters['series']
            df = df[selected_series]
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if 'price_fcst' in df.columns:
            ax.plot(df['date'] + ' ' + df['time'].astype(str), df['price_fcst'], label='Price Forecast', color='blue')
        
        if 'actual_price' in df.columns:
            ax.plot(df['date'] + ' ' + df['time'].astype(str), df['actual_price'], label='Actual Price', color='green')
        
        ax.set_xlabel('Date Time')
        ax.set_ylabel('Price')
        ax.legend()
        ax.set_title('Price Forecast vs Actual Price')
        # Rotate x-axis labels
        plt.xticks(rotation=90)

        
        # Save plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        return send_file(img, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/rmse_graph', methods=['POST'])
def generate_rmse_graph():
    try:
        filters = request.get_json()
        df = pd.read_csv('data/team_name1_price_fcst_with_actual.csv')
        
        # Ensure date is treated as string
        df['date'] = df['date'].astype(str)
        
        if 'date_range' in filters:
            start_date, end_date = filters['date_range']
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        if 'actual_price' in df.columns and 'price_fcst' in df.columns:
            grouped = df.groupby('date')
            rmse_results = {}

            for name, group in grouped:
                rmse = ((group['actual_price'] - group['price_fcst']) ** 2).mean() ** 0.5
                rmse_results[name] = rmse
            
            # Plotting RMSE
            fig, ax = plt.subplots(figsize=(10, 6))
            dates = list(rmse_results.keys())
            rmses = list(rmse_results.values())
            
            ax.plot(dates, rmses, label='RMSE', color='red')
            ax.set_xlabel('Date')
            ax.set_ylabel('RMSE')
            ax.set_title('RMSE over Time')
            ax.legend()
            
            # Save plot to a BytesIO object
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plt.close()
            
            return send_file(img, mimetype='image/png')
        else:
            return jsonify({"error": "The filtered data does not include 'actual_price' or 'price_fcst' column."})
    except Exception as e:
        return jsonify({"error": str(e)})
