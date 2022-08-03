# SDIC Individual Project Yintai Ding

#### Last Update: 03/08/2022

Now the GUI could recognise the formula input like 'CH4' but for other cases like 'CHHHH' is not available. This could be solved but there might be a lot of bugs behind :( so I leave it as unsolved.

Whats' new: 

(03/08/2022)Now some test cases are added and users could test some functions via command 'pytest'. But this test file can only test some functions but not the GUI.

(01/08/2022)Now users could upload or edit BEB Total Ionization Cross Sections via new button 'Edit TICS'.

(01/08/2022)Now the show_fragments widget includes a text browser that includes possible missing fragments. These possible missing fragments are generated by algorithm bases on chemical bonds within molecules and the generation process is totally theoretically. 

(29/07/2022)Now the requirements.txt is available.

(28/07/2022)Now the show_fragments page could load BEB total ionization cross section for each molecule at 70 eV and show partial ionization cross section for each branching ratio. And on Option page the branching ratio in table will be recalculated base on users' input of peak height. This will make sure the total branching ratio for each molecule will sum up to 1.

------------

## Introduction

--------------

This repository is used as a backup on Github for [Yintai Ding](https://github.com/Yintai-Ding/SDIC-Project-YintaiDing)'s postgraduate individual project. The full name of the project is **'Partial Ionization Cross Sections MSc Project'** and the belongs to **Unversity College London, MSc Scientific and Data Intensive Computing**. This project is supervised by Prof. Jonathan Tennyson and Dr. Bridgette Copper.

This project has two main components. The first is obtain mass spectrum data from the [NIST chemical web book](https://webbook.nist.gov/chemistry/) and the second part is to design a user friendly graphical interface to interact with the database. The first part is completed by Lifeng Luo and the second is maintained by Yintai Ding. 

## Instructions for Usage

--------------

There is a zip which name is'**data-20.zip**' inside of the tag '**Database**'which users should download and decompress to find the database. Remember to move the '**data-20.db**' file to the folder '**SDIC Project**' or users could change file path in the program manually. 

Within the '**SDIC Project**' folder there are two subfolder '**elements**' and '**geometries**'. These folders contains information for elements and relative position for atoms in sample molecules which are necessary to check the validation of data in the database. The '**fragments_generation.py**' contains functions help checking the validation of data. If the users wants to check the validation of the data in the provided database, they could run the file '**test_case.py**' by: 

```Bash
$ python test_cases.py
```

![test_case]

The first row of this code will show the users the intersection of the data generated by theoritical functions and the data gathered by mass spectrum. The second and the third will provide the difference of two methods. These will help users to check if any fragment is not reasonable to be negelected by mass spectrum. The screenshot is an example of 'Carbon Tetrachloride'. However the current data will not support for checking all seven thousands molecules. So just few special cases could be checked and need to edit the input inside of the code.

There are three ui files 'Options.ui', 'brief sample.ui' and 'show_fragments.ui' which is generated by QtDesigner. If users wants to reedit the ui outlook please load the file in QtDesigner or open the related py file and edit them directly. 

The main interface is in the '**brief sample.py**'. To open the interface, please open the file in your python compiler and run the code

![main_UI]

As shown above, users could choose their input of molecule as '*name*', '*cas number*' and '*formula*'. 

![checkbox]

After ticking the "*Calculate branching ratio for all possible fragments*" users could click the '*Run*' button to show the result of fragments. Here we use '*Methane*' as a sample: 

![show_fragments]

Here we could check the possible fragments for different charge_mass ratios and their corresponding branching ratios. On the right side of the table is partial ionization cross sections for these possible fragments. This PICS is calculated by total ionization cross sections of molecules at 70 eV. These data is gathered from the NIST webpage with the electron energy to be 70 eV. 

Now the data for total ionization cross sections and relative position of molecules is rather limited. Not all molecules could be promised to assigned for complete information. If the total ionization cross section or the relative position is missing, the table will show users noticing messages as:

![no_data]

If user forget to tick the check box, the GUI will show a reminding message on screen:

![noCheckBox]

However, there are cases that users input a wrong name or informal format of formula which is not exist in the current database. When a wrong input happened, the GUI will return a messagebox with relative message about input. Such as:

![wrongInput]

There are also cases that a formula exist isomers such as 'C6H6' may represents 'Benzene' or '1,5-Hexadiyne'. When user input a formula with isomers, GUI will also show a error message inclued names of isomers on screen:

![isomers]

If users have experimental data which might be more accurate and want to upload to the database, they could clicked on the '*Options*' button and input the data manually. For the users convenience, they could input the name or CAS number on the main page and click the '*Options*' button. Then the current data(only 70 eV) in database will be printed in the table. For now, users could edit the data directly instead of key in details step by step.

![options]

In this interface, users should input the electron energy level in the first line edit first. To input the experimental data, they should fill the elements row by row. If some data like '*cas number*' is missing, please just ignore and leave it empty. If several rows need to be recorded simultaneously, users could click the button '*Add Row*' and click '*Remove Row*' if some data is not needed. Remember to click the button '***Update***' before submit your data. Now the submit button is frozen before user click on '*Update*' to refresh the table. 

![submitOptions]

Just like the sreenshot above, when click the '*Submit*' button, a message box will comfirm the user input has been saved. But the user-input data will not be saved to the database directly. It will be saved on a temporary database names 'temp.db' and wait further manual check by data maintenance members. 

Back to the main UI, there is a new button in the bottom of the window names '*Update*' which is left for members to check the user-input data manually. To block the data from users, we set a little check question to identify members and users.

![questions]

The answer is quite easy(and is show on screen :) ) but this widget is left as block. When a incorrect answer is inputed a message will also be shown on screen:

![denied]

When the correct answer is recognised, user will see a window like:

![doubleCheck]

Currently the 'temp.db' exist some data we just upload few minutes before about Methane. The first line will show users how many tables are currently waiting for check and click on the combo box could change different table. After click on the '*Load*' button the table will be print to screen:

![checkDetail]

Just like the buttons on Option page, users could delete current lines or even delete the current table from the 'temp.db'. User should notice that '*Delete Line*' will only delete current line in this page but not delete the line in 'temp.db'. After click on the '*Submit*' button on the bottom, the data will be merged with the data in database 'data-20.db'.

Just as the possible fragments and branching ratios could be edited by users, The BEB Total Ionization Cross Sections could also be edited by users if they have more accurate data. Similar to the '*Options*' button, users could load and edit the TICS data in database via clicking on '*Edit TICS*' button. All the TICS and relative energy level will be printed to screen as:

![editBEB]

Users could add a new row or delete selected row by clicking corresponding buttons. Don't forget to activate the '*Submit*' button by clicking on '*Update*' and the data will be merged to database after submit. In case of misclick, the program will show a message box before merging the data.

[main_UI]: /SDIC%20Project/main_UI.png
[show_fragments]: /SDIC%20Project/showFragments.png
[options]: /SDIC%20Project/options.png
[checkbox]: /SDIC%20Project/checkbox.png
[checkDetail]: /SDIC%20Project/checkDetail.png
[denied]: /SDIC%20Project/denied.png
[doubleCheck]: /SDIC%20Project/doubleCheck.png
[questions]: /SDIC%20Project/questions.png
[submitOptions]: /SDIC%20Project/submitOptions.png
[noCheckBox]: /SDIC%20Project/noCheckBox.png
[wrongInput]: /SDIC%20Project/wrongInput.png
[isomers]: /SDIC%20Project/isomers.png
[test_case]: /SDIC%20Project/test_case.png
[no_data]: /SDIC%20Project/NoDataFound.png
[editBEB]: /SDIC%20Project/editBEB.png