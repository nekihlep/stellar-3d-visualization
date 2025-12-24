import pandas as pd
import numpy as np
df = pd.read_csv('HYG.csv')
print(f"Всего строк: {len(df):,}")

useful_col = ['proper', 'dist', 'mag', 'absmag', 'spect', 'lum', 'con']
df_new = df[useful_col].copy()

df_naked_eye = df_new[df_new['mag'] < 6].copy()

df_telescope = df_new[(df_new['mag'] >= 6) & (df_new['mag'] < 8)].copy()

def filter_stars(df_subset):
    mask = (
            (df_subset['dist'] > 0) &
            (df_subset['dist'] <= 300) &
            (df_subset['spect'].notna()) &
            (df_subset['con'].notna()) &
            (df_subset['lum'].notna())
    )

    df_filtered = df_subset[mask].copy()
    df_filtered['proper'] = df_filtered['proper'].fillna('')

    rename_mask = df_filtered['proper'].isna() | (df_filtered['proper'].str.strip() == '')
    df_filtered.loc[rename_mask, 'proper'] = df_filtered.loc[rename_mask, 'con'] + ' star ' + \
                                             df_filtered.loc[rename_mask].groupby('con').cumcount().add(1).astype(str)

    df_filtered = df_filtered.sort_values('mag').reset_index(drop=True)

    df_filtered['x'] = df_filtered['dist']
    df_filtered['y'] = -df_filtered['mag']
    df_filtered['z'] = -df_filtered['absmag']

    return df_filtered


df_naked_eye_final = filter_stars(df_naked_eye)
df_telescope_final = filter_stars(df_telescope)

df_telescope_final = df_telescope_final.iloc[::5]

print("ДЛЯ НЕВООРУЖЕННОГО ГЛАЗА (mag < 6):")
print(f"Всего звёзд: {len(df_naked_eye_final):,}")
print(f"Самые близкие: {df_naked_eye_final['dist'].min():.1f} пк, самые далёкие: {df_naked_eye_final['dist'].max():.1f} пк")

print("ДЛЯ ТЕЛЕСКОПА (6 ≤ mag < 8 каждая 5я звезда):")
print(f"Всего звёзд: {len(df_telescope_final):,}")
print(f"Самые близкие: {df_telescope_final['dist'].min():.1f} пк, самые далёкие: {df_telescope_final['dist'].max():.1f} пк")

__all__ = ['df_naked_eye_final', 'df_telescope_final']