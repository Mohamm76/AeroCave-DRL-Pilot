# 1. استخدام بيئة Node مستقرة
FROM node:20-alpine

# 2. تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# 3. نسخ ملفات الحزم أولاً لتسريع عملية البناء
COPY package*.json ./

# 4. تثبيت المكتبات
RUN npm install

# 5. نسخ بقية كود المشروع
COPY . .

# 6. فتح المنفذ 3000 الخاص بـ React
EXPOSE 3000

# 7. أمر التشغيل
CMD ["npm", "start"]