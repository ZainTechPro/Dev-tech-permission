from flask import Blueprint, request, jsonify
import pandas as pd
import os
import json
from datetime import datetime

permissions_bp = Blueprint('permissions', __name__)

# مسار ملف Excel
EXCEL_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'permissions_data.xlsx')

@permissions_bp.route('/permissions/load', methods=['GET'])
def load_permissions():
    """تحميل البيانات من ملف Excel"""
    try:
        if os.path.exists(EXCEL_FILE_PATH):
            df = pd.read_excel(EXCEL_FILE_PATH)
            
            # تحويل البيانات إلى التنسيق المطلوب
            users = df['User Name'].unique().tolist()
            folders = df['Folder Name'].unique().tolist()
            
            permissions = {}
            for user in users:
                permissions[user] = {}
                user_data = df[df['User Name'] == user]
                for _, row in user_data.iterrows():
                    folder = row['Folder Name']
                    # تحديد نوع الصلاحية بناءً على الأعمدة
                    if row.get('Full Control', False):
                        permission_type = 'Full Control'
                    elif row.get('Modify Access', False):
                        permission_type = 'Modify/Change'
                    elif row.get('Read Access', False):
                        permission_type = 'Read'
                    else:
                        permission_type = 'None (بدون صلاحية)'
                    
                    permissions[user][folder] = permission_type
            
            return jsonify({
                'success': True,
                'data': {
                    'users': users,
                    'folders': folders,
                    'permissions': permissions
                }
            })
        else:
            # إنشاء ملف Excel جديد بالبيانات الافتراضية
            default_data = create_default_excel()
            return jsonify({
                'success': True,
                'data': default_data,
                'message': 'تم إنشاء ملف Excel جديد بالبيانات الافتراضية'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@permissions_bp.route('/permissions/save', methods=['POST'])
def save_permissions():
    """حفظ البيانات في ملف Excel"""
    try:
        data = request.get_json()
        users = data.get('users', [])
        folders = data.get('folders', [])
        permissions = data.get('permissions', {})
        
        # إنشاء قائمة البيانات لـ DataFrame
        excel_data = []
        for user in users:
            for folder in folders:
                permission_type = permissions.get(user, {}).get(folder, 'None (بدون صلاحية)')
                
                # تحويل نوع الصلاحية إلى أعمدة منطقية
                row = {
                    'User Name': user,
                    'Folder Name': folder,
                    'Read Access': permission_type in ['Read', 'Modify/Change', 'Full Control'],
                    'Write Access': permission_type in ['Modify/Change', 'Full Control'],
                    'Modify Access': permission_type in ['Modify/Change', 'Full Control'],
                    'Delete Access': permission_type in ['Modify/Change', 'Full Control'],
                    'Full Control': permission_type == 'Full Control',
                    'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                excel_data.append(row)
        
        # إنشاء DataFrame وحفظه
        df = pd.DataFrame(excel_data)
        df.to_excel(EXCEL_FILE_PATH, index=False)
        
        return jsonify({
            'success': True,
            'message': 'تم حفظ البيانات بنجاح في ملف Excel'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@permissions_bp.route('/permissions/export', methods=['GET'])
def export_permissions():
    """تصدير البيانات كملف JSON"""
    try:
        if os.path.exists(EXCEL_FILE_PATH):
            df = pd.read_excel(EXCEL_FILE_PATH)
            
            # تحويل البيانات إلى JSON
            users = df['User Name'].unique().tolist()
            folders = df['Folder Name'].unique().tolist()
            
            permissions = {}
            for user in users:
                permissions[user] = {}
                user_data = df[df['User Name'] == user]
                for _, row in user_data.iterrows():
                    folder = row['Folder Name']
                    if row.get('Full Control', False):
                        permission_type = 'Full Control'
                    elif row.get('Modify Access', False):
                        permission_type = 'Modify/Change'
                    elif row.get('Read Access', False):
                        permission_type = 'Read'
                    else:
                        permission_type = 'None (بدون صلاحية)'
                    
                    permissions[user][folder] = permission_type
            
            export_data = {
                'users': users,
                'folders': folders,
                'permissions': permissions,
                'exported_at': datetime.now().isoformat()
            }
            
            return jsonify({
                'success': True,
                'data': export_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'ملف Excel غير موجود'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def create_default_excel():
    """إنشاء ملف Excel بالبيانات الافتراضية"""
    default_folders = [
        '\\\\10.0.11.110\\d\\0-Contracts',
        '\\\\10.0.11.110\\d\\1-CLM',
        '\\\\10.0.11.110\\d\\2-EVER WEST',
        '\\\\10.0.11.110\\d\\3- Ever new Cairo',
        '\\\\10.0.11.110\\d\\4- COM-16',
        '\\\\10.0.11.110\\d\\5- East Side',
        '\\\\10.0.11.110\\d\\6- CRM Data',
        '\\\\10.0.11.110\\d\\7- Marketing Data',
        '\\\\10.0.11.110\\d\\8-Annex',
        '\\\\10.0.11.110\\d\\9-Handing over',
        '\\\\10.0.11.110\\d\\10- CASTLE COMMERCIAL 6A',
        '\\\\10.0.11.110\\d\\11- Cred Sales Center',
        '\\\\10.0.11.110\\d\\12- Monthly reports',
        '\\\\10.0.11.110\\d\\13- projects BUA\'S',
        '\\\\10.0.11.110\\d\\14-Alaman Plot',
        '\\\\10.0.11.110\\d\\15- CRED HQ- Modifications',
        '\\\\10.0.11.110\\d\\16-CRED- Documents',
        '\\\\10.0.11.110\\d\\17-Environmental Studies- CLM-EST-COM-16',
        '\\\\10.0.11.110\\d\\18- Change request temp',
        '\\\\10.0.11.110\\d\\19- Suppliers',
        '\\\\10.0.11.110\\d\\20- CRED TEmp'
    ]
    
    default_users = [
        'Nour Mohamed Saleh Aly',
        'Ahmed Safwat Mahdly',
        'Ahmed Saleh Elwakel',
        'Amgad Thabet',
        'Fahmy Mansour',
        'Marwa Saleh',
        'Mirna Fayez',
        'Mohamed Essam',
        'Mohamed Hamada',
        'Mohamed Hassan Sadek',
        'Nader Hegab',
        'Sara Khaled',
        'Hany Abuelella',
        'Andrew Alaa Asaad',
        'Anthony Ayman Sobhy'
    ]
    
    # إنشاء البيانات الافتراضية
    excel_data = []
    permissions = {}
    
    for user in default_users:
        permissions[user] = {}
        for folder in default_folders:
            permissions[user][folder] = 'None (بدون صلاحية)'
            row = {
                'User Name': user,
                'Folder Name': folder,
                'Read Access': False,
                'Write Access': False,
                'Modify Access': False,
                'Delete Access': False,
                'Full Control': False,
                'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            excel_data.append(row)
    
    # حفظ الملف
    df = pd.DataFrame(excel_data)
    df.to_excel(EXCEL_FILE_PATH, index=False)
    
    return {
        'users': default_users,
        'folders': default_folders,
        'permissions': permissions
    }

