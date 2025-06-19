#!/usr/bin/env python3
"""
Script untuk mengkonversi file txt ke PDF menggunakan reportlab
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def txt_to_pdf(txt_file, pdf_file):
    """
    Konversi file txt ke PDF
    """
    try:
        # Read text file
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter
        
        # Set initial position
        y_position = height - 50
        line_height = 14
        margin = 50
        max_width = width - 2 * margin
        
        # Split content into lines
        lines = content.split('\n')
        
        for line in lines:
            # Check if we need a new page
            if y_position < 50:
                c.showPage()
                y_position = height - 50
            
            if line.strip():
                # Handle long lines by wrapping them
                wrapped_lines = simpleSplit(line, "Helvetica", 10, max_width)
                
                for wrapped_line in wrapped_lines:
                    if y_position < 50:
                        c.showPage()
                        y_position = height - 50
                    
                    c.drawString(margin, y_position, wrapped_line)
                    y_position -= line_height
            else:
                # Empty line
                y_position -= line_height / 2
        
        c.save()
        print(f"✅ Converted: {txt_file} -> {pdf_file}")
        
    except Exception as e:
        print(f"❌ Error converting {txt_file}: {e}")

def convert_all_txt_to_pdf(folder_path="pdf_documents"):
    """
    Konversi semua file .txt ke .pdf dalam folder
    """
    if not os.path.exists(folder_path):
        print(f"❌ Folder {folder_path} tidak ditemukan.")
        return
    
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"❌ Tidak ada file .txt ditemukan dalam folder {folder_path}")
        return
    
    print(f"📄 Ditemukan {len(txt_files)} file .txt untuk dikonversi:")
    
    for txt_file in txt_files:
        txt_path = os.path.join(folder_path, txt_file)
        pdf_file = txt_file.replace('.txt', '.pdf')
        pdf_path = os.path.join(folder_path, pdf_file)
        
        print(f"🔄 Converting: {txt_file}")
        txt_to_pdf(txt_path, pdf_path)
    
    print(f"\n🎉 Selesai! {len(txt_files)} file telah dikonversi ke PDF.")

if __name__ == "__main__":
    print("📄 Konversi file TXT ke PDF...")
    convert_all_txt_to_pdf()
