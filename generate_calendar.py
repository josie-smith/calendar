# -*- coding: utf-8 -*-
"""
Python LaTeX monthly Mon-Sun calendar generator. This script is able to generate A3
landscape monthly clalendar Monday to Sunday using pdfLaTeX. PdfLaTeX is hence
required to run this script.

@author Josie Smith
Created 14/12/2020
"""

import calendar
import datetime
import os
import sys
from dateutil.easter import *
path = os.path.abspath(os.path.dirname(sys.argv[0]))

def print_month(year,month_number):
    """ This function generate a .tex file and print a .pdf A3
    landscape monthly clalendar Monday to Sunday using pdfLaTeX of a specific
    year(xxxx) and month (1-12)
    """
    create_events(year)
    monthname=str(calendar.month_name[month_number])

    #start writing on a .tex file
    with open(path+'/'+str(year)+'.tex','w') as f:
        f.write(r'\documentclass[landscape,12pt]{article}'+'\n')
        f.write(r'\usepackage[landscape,a3paper,margin=0.5in]{geometry}'+'\n')
        f.write(r'\usepackage{array}'+'\n')
        f.write(r'\usepackage{tabularx}'+'\n')
        f.write(r'\usepackage{fix-cm} '+'\n')
        f.write(r'\usepackage[notmath]{sansmathfonts}'+'\n')
        f.write(r'\newcolumntype{R}{>{\raggedleft\arraybackslash}X}'+'\n')
        f.write(r'\makeatletter'+'\n')
        f.write(r'\newcommand\HUGE{\@setfontsize\Huge{45}{50}}'+'\n')
        f.write(r'\makeatother'+'\n')
        f.write('\n')
        f.write(r'\begin{document}'+'\n')
        f.write(r'\pagestyle{empty} % Removes the page number from the bottom of the page '+'\n')
        f.write(r'\noindent'+'\n')
        f.write(r'\sffamily'+'\n')
        f.write('\n')

        generate_month(year, month_number, f)

        f.write(r'\end{document}' +'\n')

    os.system('pdflatex '+monthname+str(year)+'.tex')
    os.remove(monthname+str(year)+'.aux')
    os.remove(monthname+str(year)+'.log')
    os.remove(monthname+str(year)+'.tex')

def generate_month(year,month_number, f):
    print('Month: ' + str(month_number))

    week=0
    monthname=str(calendar.month_name[month_number])
    cal=calendar.Calendar()
    month=cal.itermonthdays(year,month_number) #month is an iterable generator
    month = list(month)
    first_7_element=month[:7]
    extrarowheight='15'
    cellheight='70'
    tabcolsep='15'

    if first_7_element==[1,2,3,4,5,6,7]:
        if month_number==2:
            cellheight='100' #in this particular case we need only 4 rows so we can add some more height
        else:
           pass

    if len(month) >= 35 :
        for i in range (35, len(month)):
            if month[i] != 0 :
                month[i-35] = month[i]
    print(month)

    f.write(r'\center{\textsc{\HUGE %s} \textsc{\LARGE %s}}' %(monthname,str(year))+'\n')
    f.write(r'\vspace{20pt}'+'\n')
    f.write('\n')
    f.write('\n')
    f.write(r'\setlength{\tabcolsep}{59pt}'+'\n')
    f.write(r'\begin{tabular}{c c c c c c c }'+'\n')
    f.write(r' Monday &  Tuesday & Wednesday  & Thursday & Friday & Saturday & Sunday \\'+'\n ')
    f.write(r' \end{tabular}'+'\n')
    f.write('\n')
    f.write(r'\setlength{\tabcolsep}{%spt}'%(tabcolsep)+'\n')
    f.write(r'\setlength{\extrarowheight}{%spt}'%(extrarowheight)+'\n')
    f.write(r'\begin{tabularx}{\textwidth}[t]{|R|R|R|R|R|R|R|}'+'\n')
    f.write(r'\hline     \begin{tabular}{@{}r@{}}\large{')

    count=1
    for i in month:
        # print (count,i)
        # print ('WEEK:',week)
        if (count==7 and week==4) or (count==7 and i==28 and month_number==2):
            if i==0:
                f.write(r' }\\[%spt]'%(cellheight)+r' \normalsize{}\\[-5mm] \normalsize{}\\[-10pt] \end{tabular}\\'+'\n \hline')
                count+=1
            else:
                if long(event[(i,month_number)]) : cellheight = str(int(cellheight) - 25)
                f.write(str(i)+r'}\\[%spt]'%(cellheight)+r' \normalsize{' + event[(i,month_number)] + r'}\\[-10pt] \end{tabular}\\'+'\n\hline')
                if long(event[(i,month_number)]) : cellheight = str(int(cellheight) + 25)
                count+=1
            break
        else:
            if i==0: #we don't want to see zeros around the tables!!
                f.write(' '+r'} \\[%spt]'%(cellheight)+r' \normalsize{}\\[-5mm] \normalsize{}\\[-10pt] \end{tabular}'+'\n\t'+r'& \begin{tabular}{@{}r@{}}\large{')
                count+=1
            elif count%7==0:
                if long(event[(i,month_number)]) : cellheight = str(int(cellheight) - 25)
                f.write(str(i)+r'}\\[%spt]'%(cellheight)+r' \normalsize{' + event[(i,month_number)]  + r'}\\[-10pt] \end{tabular}\\'+'\n'+r'\hline  \begin{tabular}{@{}r@{}}\large{') #new row in LaTeX
                if long(event[(i,month_number)]) : cellheight = str(int(cellheight) + 25)
                count=1
                week+=1
            else: # new element
                if long(event[(i,month_number)]) : cellheight = str(int(cellheight) - 25)
                f.write(str(i)+r'}\\[%spt]'%(cellheight)+r' \normalsize{' + event[(i,month_number)]  + r'}\\[-10pt] \end{tabular}'+'\n\t'+r' & \begin{tabular}{@{}r@{}}\large{')
                if long(event[(i,month_number)]) : cellheight = str(int(cellheight) + 25)
                count+=1
    f.write(r'\end{tabularx}'+'\n')

def print_year(year,start=1,stop=12):
    create_events(year)

    #start writing on a .tex file
    with open(path+'/'+str(year)+'.tex','w') as f:
        f.write(r'\documentclass[landscape,12pt]{article}'+'\n')
        f.write(r'\usepackage[landscape,a3paper,margin=0.5in]{geometry}'+'\n')
        f.write(r'\usepackage{array}'+'\n')
        f.write(r'\usepackage{tabularx}'+'\n')
        f.write(r'\usepackage{fix-cm} '+'\n')
        f.write(r'\usepackage[notmath]{sansmathfonts}'+'\n')
        f.write(r'\newcolumntype{R}{>{\raggedleft\arraybackslash}X}'+'\n')
        f.write(r'\makeatletter'+'\n')
        f.write(r'\newcommand\HUGE{\@setfontsize\Huge{45}{50}}'+'\n')
        f.write(r'\makeatother'+'\n')
        f.write('\n')
        f.write(r'\begin{document}'+'\n')
        f.write(r'\pagestyle{empty} % Removes the page number from the bottom of the page '+'\n')
        f.write(r'\noindent'+'\n')
        f.write(r'\sffamily'+'\n')
        f.write('\n')

        for i in range(start,stop+1):
            generate_month(year, i, f)
            f.write(r'\newpage' +'\n')

        f.write(r'\end{document}' +'\n')

    os.system('pdflatex '+str(year)+'.tex')
    os.remove(str(year)+'.aux')
    os.remove(str(year)+'.log')
    os.remove(str(year)+'.tex')

def create_events(year):
    # initialise events
    global event
    event = {}
    for month in range(1, 13):
        for day in range(1, 32):
            event[(day,month)] = r"}\\[-5mm] \normalsize{"

    event[(1,1)] += r"New Year's Day}\\[-5mm] \normalsize{"
    event[(2,1)] += r"Day After New Year's Day}\\[-5mm] \normalsize{"
    event[(6,2)] += r"Waitangi Day}\\[-5mm] \normalsize{"
    event[(mothers_day(year).day, mothers_day(year).month)] += r"UK Mother's Day}\\[-5mm] \normalsize{"
    event[(easter(year).day-2, easter(year).month)] += r"Good Friday}\\[-5mm] \normalsize{"
    event[(easter(year).day, easter(year).month)] += r"Easter Sunday}\\[-5mm] \normalsize{"
    event[(easter(year).day+1, easter(year).month)] += r"Easter Monday}\\[-5mm] \normalsize{"
    event[(25,4)] += r"ANZAC Day}\\[-5mm] \normalsize{"
    event[(nth_day(1, 1, year, 6),6)] += r"Queen's Birthday}\\[-5mm] \normalsize{"
    event[(nth_day(3, 7, year, 6),6)] += r"UK Father's Day}\\[-5mm] \normalsize{"
    event[(nth_day(2, 3, year, 10),10)] += r"Labour Day}\\[-5mm] \normalsize{"
    event[(nth_day(2, 5, year, 11, 2),11)] += r"North Canterbury}\\[-5mm] \normalsize{Anniversary Day}\\[-5mm] \normalsize{"
    event[(25,12)] += r"Christmas Day}\\[-5mm] \normalsize{"
    event[(26,12)] += r"Boxing Day}\\[-5mm] \normalsize{"

    # Add you own custom events here

def mothers_day(year) :
    return easter(year) + datetime.timedelta(days=-21)

def nth_day(n, day, year, month, following=0) :
    # returns the date of the {n}th {day} following the first {following}
    if following == 0: following = day
    cal=calendar.Calendar()
    month_weeks = cal.monthdatescalendar(year, month)
    week = month_weeks[n-1]
    if month_weeks[0][following-1].month != month:
        week = month_weeks[n]
    date = week[day-1]
    return date.day

def long(event) :
    # TODO manage cases with more than 2 events on a day
    return event.count(r"\normalsize") > 1

print_year(2021)
