#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
import wave
import numpy as np

def save_wav(path, data, mono=True):
    """
    wav形式のデータを保存する関数．
    
    Parameters
    ----------
    path : str
        保存先へのパス
    data : ndarray
        信号の配列
    """
    if mono:
        channels = 1  # mono
    else:
        channels = 2  # stereo
        
    binwave = struct.pack('h' * len(data), *data)  # バイナリ化

    with wave.Wave_write(path) as wav:
        # チャンネル数(1:モノラル,2:ステレオ)，サンプルサイズ(バイト)，サンプリング周波数，フレーム数
        params = (channels, 2, 16000, len(binwave), 'NONE', 'not compressed')
        wav.setparams(params)
        wav.writeframes(binwave)

def dft(start, x, N):
    """
    xのstartサンプル目からのNサンプルを周期波形とみなしたDFT値を返す
    
    Parameters
    ----------
    start : int
        処理の開始位置
    x : array
        入力信号
    N : int
        DFTを行う点数
    
    returns
    ----------
    X : array
        DFTの結果
    """
    
    X = [0.0] * N
    for k in range(N):
        for n in range(N):
            real = np.cos(2 * np.pi * k * n / N)
            imag = - np.sin(2 * np.pi * k * n / N)
            X[k] += x[start + n] * complex(real, imag)
    return X

def get_db_hz(x):
    """
    離散フーリエ変換を用いて，周波数とそのパワースペクトルを得る関数．
    
    Parameter
    ----------
    x : array
        信号
    
    returns
    ----------
    db : array
        パワースペクトル
    hz : array
        周波数
    """
    
    F = dft(0, x, 1000)      # 離散フーリエ変換(DFT)
    amp = np.abs(F)            # 振幅スペクトル
    power = amp ** 2           # パワースペクトル(振幅スペクトルの二乗)
    db = 10 * np.log10(power)  # 利得

    hz = []
    for i, _ in enumerate(F):
        hz.append(16000 * (i / 1000))  # 周波数(Hz)

    return db, hz
