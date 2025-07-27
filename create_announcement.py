#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import os

def create_announcement_pdf():
    # إنشاء ملف PDF
    c = canvas.Canvas("announcement.pdf", pagesize=A4)
    width, height = A4
    
    # إعداد الخط العربي (سنستخدم خط افتراضي)
    c.setFont("Helvetica-Bold", 24)
    
    # العنوان الرئيسي
    title = "إعلان"
    title_width = c.stringWidth(title, "Helvetica-Bold", 24)
    c.drawString((width - title_width) / 2, height - 100, title)
    
    # العنوان الفرعي
    c.setFont("Helvetica-Bold", 16)
    subtitle = "صادر عن سلطة وادى الأردن"
    subtitle_width = c.stringWidth(subtitle, "Helvetica-Bold", 16)
    c.drawString((width - subtitle_width) / 2, height - 140, subtitle)
    
    # النص الرئيسي
    c.setFont("Helvetica", 12)
    text = """تطلب سلطة وادي الأردن من السادة المبينة اسماؤهم بادناه مراجعتها في مبناها الكائن في منطقة الشميساني خلف فندق الماريوت مبنى وزارة المياه والري سلطة وادي الاردن الطابق الثاني مديرية الموارد البشرية حسب التاريخ والوظيفة المبينه ازاء اسم كلاً منهم في تمام الساعة العاشرة صباحاً لاجل اجراء المقابلة الشخصية من اجل التعيين بعقد محدد المدة مصطحبين معهم هوية الاحوال المدنية سارية المفعول على ان يكون الحضور قبل موعد المقابلة بساعة ."""
    
    # تقسيم النص إلى أسطر
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if c.stringWidth(test_line, "Helvetica", 12) < width - 100:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    # رسم النص
    y_position = height - 200
    for line in lines:
        c.drawString(50, y_position, line)
        y_position -= 20
    
    # عنوان قائمة المرشحين
    c.setFont("Helvetica-Bold", 14)
    candidates_title = "أسماء المرشحين للمقاولات"
    candidates_width = c.stringWidth(candidates_title, "Helvetica-Bold", 14)
    c.drawString((width - candidates_width) / 2, y_position - 40, candidates_title)
    
    # مساحة لقائمة الأسماء
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position - 80, "[قائمة الأسماء والتفاصيل ستظهر هنا]")
    
    c.save()
    print("تم إنشاء ملف announcement.pdf بنجاح!")

if __name__ == "__main__":
    create_announcement_pdf()