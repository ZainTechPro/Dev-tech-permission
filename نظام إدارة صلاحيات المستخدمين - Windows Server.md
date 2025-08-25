# نظام إدارة صلاحيات المستخدمين - Windows Server

نظام ويب لإدارة صلاحيات المستخدمين على مجلدات Windows Server مع حفظ البيانات في ملف Excel.

## المميزات

- واجهة ويب سهلة الاستخدام باللغة العربية
- حفظ البيانات في ملف Excel محلياً
- إدارة المستخدمين والمجلدات
- تحديد أنواع الصلاحيات (None, Read, Modify, Full Control)
- تصدير واستيراد البيانات
- حماية الخصوصية - جميع البيانات محلية

## متطلبات التشغيل

- Python 3.11+
- Flask
- pandas
- openpyxl

## طريقة التشغيل

1. تحميل المشروع:
```bash
git clone <repository-url>
cd permissions_api
```

2. تفعيل البيئة الافتراضية:
```bash
source venv/bin/activate
```

3. تشغيل الخادم:
```bash
python src/main.py
```

4. فتح المتصفح على:
```
http://localhost:5000
```

## هيكل المشروع

```
permissions_api/
├── src/
│   ├── static/
│   │   └── index.html          # الواجهة الأمامية
│   ├── routes/
│   │   ├── permissions.py      # API endpoints
│   │   └── user.py
│   ├── models/
│   │   └── user.py
│   └── main.py                 # نقطة البداية
├── venv/                       # البيئة الافتراضية
├── requirements.txt            # المتطلبات
├── permissions_data.xlsx       # ملف البيانات (يتم إنشاؤه تلقائياً)
└── README.md
```

## API Endpoints

- `GET /api/permissions/load` - تحميل البيانات من Excel
- `POST /api/permissions/save` - حفظ البيانات في Excel
- `GET /api/permissions/export` - تصدير البيانات كـ JSON

## الأمان والخصوصية

- جميع البيانات محفوظة محلياً
- لا يتم إرسال أي بيانات لخوادم خارجية
- ملف Excel محمي ومحفوظ على الخادم المحلي

## الدعم الفني

للمساعدة أو الاستفسارات، يرجى التواصل مع فريق تكنولوجيا المعلومات.

