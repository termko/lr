#!/usr/bin/env python3
import os, sys, csv

THETA_FILE = 'theta'
PRICE_FILE = 'data.csv'

def theta_read():
    try:
        if os.path.isfile(os.path.join(sys.path[0],THETA_FILE)):
            theta_f = open(THETA_FILE, 'a+')
        else:
            theta_f = open(THETA_FILE, 'a+')
            theta_f.write('0 0')
    except Exception as ex:
        print('Error with opening file '+THETA_FILE+':')
        print(ex)
        exit(1)
    try:
        theta_f.seek(0)
        thetas = theta_f.read().split(' ')
        theta_0 = float(thetas[0])
        theta_1 = float(thetas[1])
    except Exception as ex:
        print('Error with getting thetas from file:')
        print(ex)
        exit(1)
    theta_f.close()
    return theta_0, theta_1

def data_read():
    try:
        price_f = open(PRICE_FILE, 'r')
    except Exception as ex:
        print('Error with opening file '+PRICE_FILE+':')
        print(ex)
        exit(1)
    try:
        csv_reader = csv.reader(price_f)
        data = []
        prices_ind = -1
        km_ind = -1
        i = 0
        for row in csv_reader:
            if i == 0:
                prices_ind = row.index('price')
                km_ind = row.index('km')
                i = 1
                continue
            data.append([float(row[km_ind]), float(row[prices_ind])])
    except Exception as ex:
        print('Error with reading file '+PRICE_FILE+':')
        print(ex)
        exit(1)
    price_f.close()
    return data

def estimate_price(km, theta_0, theta_1):
    return theta_0 + theta_1 * km

def count_precision(data, theta_0, theta_1):
    errors = []
    for row in data:
        predicted = estimate_price(row[0], theta_0, theta_1)
        actual = row[1]
        errors.append(abs(actual - predicted) / actual)
    return sum(errors) / len(errors)

def count_sum_0(data, theta_0, theta_1, lr):
    sum_0 = .0
    for row in data:
        sum_0 += estimate_price(row[0], theta_0, theta_1) - row[1]
    sum_0 /= len(data)
    return sum_0 * lr

def count_sum_1(data, theta_0, theta_1, lr):
    sum_1 = .0
    for row in data:
        sum_1 += (estimate_price(row[0], theta_0, theta_1) - row[1]) * row[0]
    sum_1 /= len(data)
    return sum_1 * lr

def train(data, theta_0, theta_1):
    error_needed = 0.0000001
    error = 1
    learning_rate = 0.0001
    i = 0
    while abs(error) > error_needed:
        tmp_theta_0 = theta_0
        tmp_theta_1 = theta_1
        sum_0 = count_sum_0(data, tmp_theta_0, tmp_theta_1, learning_rate)
        sum_1 = count_sum_1(data, tmp_theta_0, tmp_theta_1, learning_rate)
        print(sum_0, sum_1)
        tmp_theta_0 -= sum_0
        tmp_theta_1 -= sum_1
        theta_0 = tmp_theta_0
        theta_1 = tmp_theta_1
        error = count_precision(data, theta_0, theta_1)
        i += 1
        if i == 5000:
            exit(0)
        print(theta_0, theta_1)

if __name__ == '__main__':
    theta_0, theta_1 = theta_read()
    print(theta_0, theta_1)
    data = data_read()
    train(data, theta_0, theta_1)
