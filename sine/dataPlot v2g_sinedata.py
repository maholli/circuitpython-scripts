import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pandas import read_csv
# currentDir = os.getcwd()
# print('Current directory is:\n    ', currentDir)
cwd = r'C:\Users\maholli\OneDrive - Leland Stanford Junior University\Research\CircuitPython\circuitpython-scripts\sine'
# cwd = r'D:\Users\Max5TB\Documents\OneDrive - Leland Stanford Junior University\Research\Rad Protection - Biasing\rad_data\XTB RAW DATA\XTB_9days'


#Open and then read the file
# fileName = 'G:/DATA0000.CSV'
# fileName = ['DATA0001.CSV','DATA0002.CSV','DATA0003.CSV','DATA0004.CSV','DATA0005.CSV','DATA0006.CSV','DATA0007.CSV','DATA0008.CSV','DATA0009.CSV','DATA0010.CSV','DATA0011.CSV','DATA0012.CSV','DATA0013.CSV',]
# fileName = ['DATA0001.CSV','DATA0002.CSV','DATA0003.CSV','DATA0004.CSV','DATA0005.CSV']
# fileName = ['DATA0000.CSV', 'DATA0001.CSV','DATA0002.CSV','DATA0003.CSV']
# fileName = ['BoardG-100uA.CSV',  'BoardG-250uA.CSV',  'BoardI-100uA.CSV',  'BoardI-250uA.CSV']
fileName = 'sinedata.txt'
# fileName = ['DATA0005_partial.CSV', 'DATA0006.CSV']
dataSet = []



plot = True
save_plot = False
output_data = False

firstMark = True

data = open(cwd+'\\'+fileName, 'r')
for line in data:
	dataSet.append(line)


# ------ parsing datasets
# for item in fileName:	
# 	# parse the txt or csv file into data arrays
# 	data = read_csv(cwd+'\\'+item,
# 					engine='c',
# 					sep=',',
# 					header=0,
# 					# names = [0],
# 					# usecols = [0],
# 					skip_blank_lines=True,
# 					comment='#',
# 					na_filter=False,
# 					memory_map =True,
# 					float_precision='round_trip')
# 	for line in data.values:
# 		print(line)
# 		try:
# 			# label = str(line[0])
# 			# timeStamp = int(line[1])
# 			entry = float(line[0])
# 			dataSet.setdefault('S1',[])
# 			dataSet['S1'].append(entry)
# 		except:
# 			print('**** data error ****')
# 			continue
# dataSquished={}
# for key in dataSet:
# 	try:
# 		dataSquished.setdefault(key,np.array(dataSet[key]))
# 	except:
# 		print(key, '\n *** data key error... ***')
# 		continue

# print(dataSquished.keys())

# ------ Normalizing to temperature
# def crossPlot(data, temperData):
# 	tempStep, resetCount = 0, 0
# 	timeTemperature = []
# 	for i in data[:,1]:
# 		T = temperData[tempStep][1]
# 		timeTemperature.append((T,i))
# 		if resetCount > 51:
# 			tempStep += 1
# 			resetCount = 0
# 		resetCount += 1
# 	return timeTemperature
	
# def Vnormalize(data, temperData, curveFit, adjust):
# 	tempStep, resetCount = 0, 0
# 	Vnom = []
# 	T = (adjust[1] - temperData[tempStep][1])
# 	for i in data[:,1]:
# 		a = (curveFit[0]*T**2)+(curveFit[1]*T+curveFit[2])
# 		Vnom.append((((i-adjust[0])**2)*a))
# 		if resetCount > 51:
# 			tempStep += 1
# 			resetCount = 0
# 		resetCount += 1
# 	return Vnom

# # ------ smoothing function
# def smooth(func, amount):
# 	data, tempo = [],[]
# 	cnt = 1
# 	for i in func:
# 		tempo.append(i)
# 		if (cnt % amount == 0):
# 			data.append((np.sum(tempo)/amount))
# 			tempo=[]
# 			cnt = 0
# 		cnt += 1
# 	return data


# # ------ line fit 
# # a,b  = zip(*crossPlot(data3,dataT))
# # slope = np.polyfit(a, b, 2) #ax^2 + bx + c
# # abline_values = [slope[0] * i**2 + slope[1]*i + slope[2] for i in a]
# # print("Curve Fit:",slope)
# # n = Vnormalize(data3, dataT, slope, (np.average(data3[:,1]),
# # 									np.average(dataT[:,1])))
# # slope, intercept = np.polyfit(a, b, 2)
# # abline_values = [slope * i + intercept for i in a]
# # print('Slope:\t',slope,' Intercept: \t',intercept)



# # ------ Calculate time stuff
# # datagroup = dataT
# # arr = []
# # pst = datagroup[1][0]
# # for i in datagroup[:,0]:
# # 	a = i - pst
# # 	if a > 0:
# # 		arr.append(a)
# # 		pst = i

# # pst = np.average(arr)
# # print('Average Time Between Measurements:\t','%.2f' % pst,'usec')
# # print('Length of test:\t','%.2f' % ((pst/(60*1e6))*len(datagroup[:,0])),'min \t %.2f' % ((pst/(60*60*1e6))*len(datagroup[:,0])), 'hrs')
# # plot_string = 'Length of test: %.2f min' %((pst/(60*1e6))*len(datagroup[:,0])), '%.2f hrs' %((pst/(60*60*1e6))*len(datagroup[:,0]))


# # ------ output configured CSV files
# if output_data:
# 	print('Saving Data...')
# 	# np.savetxt(cwd+'\\'+"raw_temperature.csv", dataT, delimiter=",", fmt='%i %.3f', header="temperature data from:"+str(fileName))
# 	# np.savetxt(cwd+'\\'+"raw_battery.csv", 	   dataB, delimiter=",", fmt='%i %.3f', header="battery data from:"+str(fileName))
# 	# np.savetxt(cwd+'\\'+"raw_pmos1.csv", 	   data2, delimiter=",", fmt='%i %.8f', header="PMOS Vth data from:"+str(fileName))
# 	# np.savetxt(cwd+'\\'+"raw_nmos1.csv", 	   data3, delimiter=",", fmt='%i %.8f', header="NMOS Vth data from:"+str(fileName))
# 	# np.savetxt(cwd+'\\'+"raw_BoardG-100_H1.csv",dataH1, delimiter=",", fmt='%i %.8f %.8f %.8f %.8f %.8f %.8f', header="time(us), phase 1 (V), phase 2 (V), phase 3 (V), phase 4 (V), Hall V (calculated) (V), Vapplied (V), H1 from:"+str(fileName))
# 	# np.savetxt(cwd+'\\'+"raw_BoardG-100_H2.csv",dataH2, delimiter=",", fmt='%i %.8f %.8f %.8f %.8f %.8f %.8f', header="time(us), phase 1 (V), phase 2 (V), phase 3 (V), phase 4 (V), Hall V (calculated) (V), Vapplied (V), H2 from:"+str(fileName))


if plot:

	plt.rcParams['agg.path.chunksize'] = 10000
	fig, axes = plt.subplots(nrows=1, ncols=1, linewidth=0.5, figsize=(6,8))
	colors = ['maroon'
			  ]
	#all in one go:
	# ea_plot = [x[:,1] for x in dataSquished.values()]

	#individually
	# ea_plot = [smooth(dataSquished['T'][:,1], 50),	# 1
	# 		#   dataSquished['B'][:,1],	# 2
	# 		  smooth(dataSquished['R1'][:,1],100),	# 3
	# 		  smooth(dataSquished['R2'][:,1],100),	# 4
	# 		  dataSquished['N1'][:,1],	# 5
	# 		  dataSquished['P1'][:,1]	# 6
	# 		 ]
	fig, ax = plt.subplots()
	ax.plot(dataSet)
	ax.grid()
	plt.show()

	# for ax, y, c in zip(axes, ea_plot, colors):
	# 	try:
	# 		ax.plot(y, color=c)
	# 		ax.minorticks_on()
	# 		ax.tick_params(axis='both', which='both', direction='in')
	# 		# ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2E'))
	# 		# ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2E'))
	# 		ax.get_xaxis().set_visible(False)
	# 	except:
	# 		print('error', y)
	# 		continue
	# plt.tight_layout()
	# # plt.text(1.5, 0.98, plot_string, fontsize=14, transform=p1.transAxes, verticalalignment='top')	
	
	# if save_plot:
	# 	plt.savefig(cwd+'\\raw_plot.png', dpi = 300)	
	# 	print('saved at: ',str(cwd)+'\\raw_plot.png')
	# 	print()

	
	plt.show()


