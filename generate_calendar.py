# -*- coding: utf-8 -*-
"""
Python LaTeX monthly Mon-Sun calendar generator. This script is able to generate A3
landscape monthly clalendar Monday to Sunday using pdfLaTeX. PdfLaTeX is hence
required to run this script.
@author Josie Smith
Created 14/12/2020
"""

import calendar
import os
import sys
import subprocess
path = os.path.abspath(os.path.dirname(sys.argv[0]))

def print_month(year,month_number):
    print('Month: ' + str(month_number))
    """ This function generate a .tex file and print a .pdf A3
    landscape monthly clalendar Monday to Sunday using pdfLaTeX of a specific
    year(xxxx) and month (1-12)
    """
    week=0
    monthname=str(calendar.month_name[month_number])
    cal=calendar.Calendar()
    month=cal.itermonthdays(year,month_number) #month is an iterable generator
    month = list(month)
    first_7_element=month[:7]
    extrarowheight='15'
    cellheight='105'
    tabcolsep='15'

    if first_7_element==[1,2,3,4,5,6,7]:
        if month_number==2:
            cellheight='139' #in this particular case we need only 4 rows so we can add some more height
        else:
           pass

    if len(month) >= 35 :
        for i in range (35, len(month)):
            if month[i] != 0 :
                month[i-35] = month[i]
    print(month)

    #start writing on a .tex file
    with open(path+'/'+monthname+str(year)+'.tex','w') as f:
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
        f.write(r'\hline     \large{')

        count=1
        for i in month:
            # print (count,i)
            # print ('WEEK:',week)
            if (count==7 and week==4) or (count==7 and i==28 and month_number==2):
                if i==0:
                    f.write(r' }\\[%spt]'%(cellheight)+'\n'+'\hline')
                    count+=1
                else:
                    f.write(str(i)+r'}\\[%spt]'%(cellheight)+'\n'+'\hline')
                    count+=1
                break
            else:
                if i==0: #we don't want to see zeros around the tables!!
                    f.write(' '+r'}& \large{')
                    count+=1
                elif count%7==0:
                    f.write(str(i)+r'}\\[%spt]'%(cellheight)+'\n'+'\hline     \large{') #new row in LaTeX
                    count=1
                    week+=1
                else: # new element
                    f.write(str(i)+r'}& \large{')
                    count+=1
        f.write(r'\end{tabularx}'+'\n')
        f.write(r'\end{document}' +'\n')

    os.system('pdflatex '+monthname+str(year)+'.tex')
    os.remove(monthname+str(year)+'.aux')
    os.remove(monthname+str(year)+'.log')
    # os.remove(monthname+str(year)+'.tex')


def print_year(year,start=1,stop=12):
    ''''
    This function simply iterate print_month() function over a specified year.
    A narrow range of months can be printed using the others two parameters.
    '''
    for i in range(start,stop):
        print_month(year,i)

print_year(2021)
