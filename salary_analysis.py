import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Klasörleri oluştur ---
os.makedirs('outputs/figures', exist_ok=True)

# --- Veri Yükleme ---
df = pd.read_csv("data/Salary_Data.csv")

# --- Veri Keşfi ---
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())

# --- Eksik Veri Doldurma ---
df['Salary'] = df['Salary'].ffill()  # geleceğe uyumlu
df['Years of Experience'] = df['Years of Experience'].fillna(df['Years of Experience'].mean())

# --- Eğitim Seviyesi Normalizasyonu ---
df['Education Level'] = df['Education Level'].str.title().str.strip()  # 'phd' → 'Phd', boşlukları temizle

# --- Aykırı Değer Analizi (Z-score) ---
salary = df['Salary']
z_scores = (salary - np.mean(salary)) / np.std(salary)
outliers = df[(z_scores > 3) | (z_scores < -3)]
print("Aykırı Değerler:\n", outliers)

# --- Gruplama ---
print(df.groupby('Gender')['Salary'].mean())
print(df.groupby('Education Level')['Salary'].mean())
print(df.groupby(['Education Level','Years of Experience'])['Salary'].mean())

# --- Salary Band Kolonu ---
def salary_band(s):
    if s < 50000:
        return 'Low'
    elif s < 100000:
        return 'Medium'
    else:
        return 'High'

df['Salary Band'] = df['Salary'].apply(salary_band)
print(df[['Salary','Salary Band']].head())

# --- Görselleştirme ---
sns.set(style="whitegrid")

# Histogram
plt.figure(figsize=(8,5))
sns.histplot(df['Salary'], bins=15, kde=True)
plt.title("Maaş Dağılımı")
plt.savefig('outputs/figures/salary_distribution.png')
plt.show()

# Boxplot
plt.figure(figsize=(6,5))
sns.boxplot(x='Gender', y='Salary', data=df)
plt.title("Cinsiyete Göre Maaş Dağılımı")
plt.savefig('outputs/figures/gender_boxplot.png')
plt.show()

# Scatterplot
plt.figure(figsize=(8,5))
sns.scatterplot(x='Years of Experience', y='Salary', hue='Gender', data=df)
plt.title("Deneyim vs Maaş")
plt.savefig('outputs/figures/scatter_experience_salary.png')
plt.show()

# Korelasyon Heatmap
plt.figure(figsize=(6,5))
corr = df[['Age','Years of Experience','Salary']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Korelasyon Matrisi")
plt.savefig('outputs/figures/correlation_heatmap.png')
plt.show()

# --- Sonuçları Kaydetme ---
df.to_csv('outputs/Salary_Analysis_Output.csv', index=False)
df.to_excel('outputs/Salary_Analysis_Output.xlsx', index=False)
