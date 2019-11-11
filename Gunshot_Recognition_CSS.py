# Defining style sheet here for if_no_class window.
#------------------------------------------------------------------------------

styleSheetIfNoClass = """

/* **************************** BUTTONS **************************** */

QPushButton#inc_enabled[Test=true] 
{
    color:#ffffff; 
    background-color:#000000; 
    font-weight:bold; 
    border-radius:10px;
}
QPushButton#inc_enabled:hover
{
    color:#ffffff; 
    background-color:#054A73; 
    font-size:13px;
    font-weight:bold; 
    border-radius:10px;
    border: 1.5px solid #ffffff;
}
QPushButton#inc_enabled:pressed
{
    color:#000000; 
    background-color:#35BEF4; 
    border-radius:10px;
    border: 1.5px solid #000000;
}
QPushButton#inc_disabled[Test=true] 
{
    color:#000000; 
    background-color:#6B6B6B; 
    border-radius:10px;
}

/* **************************** LABELS **************************** */
QLabel#inc_title
{
    background-color:#20000000; 
}
QLabel#inc_body
{
    background-color:#191B1A; 
}
QLabel#inc_footer
{
    background-color:#80000000; 
}
QLabel#Label_title_text
{
    color:#cecece; 
    font-size:30px; 
    font-weight:bold;
}
QLabel#Label_title_sub_text
{
    color:#cecece; 
    font-size:12px; 
    font-weight:bold; 
    /*text-shadow:0px 0px 3px #FF0000;*/
    /*box-shadow:0px 0px 20px 10px #800000;*/
}
    
/* **********************  LINE EDIT **************************** */
QLineEdit#inc_classNameText
{
    color:#000000; 
    background-color:#6B6B6B; 
    border-radius:10px; 
    padding-left:23px; 
    font-size:18px; 
    font-weight:bold;
}

"""

# Defining style sheet here for main window.
#------------------------------------------------------------------------------

styleSheetMain = """

/* **************************** BUTTONS **************************** */

QPushButton#Advance_enabled[Test=true] 
{
    color:#808080; 
    background-color:#000000; 
    font-weight:bold; 
    border-top-right-radius:12px; 
    border-top-left-radius:12px;
}
QPushButton#Advance_enabled:hover
{
    color:#ffffff; 
    background-color:#000000;
    font-size:12px;
    font-weight:bold; 
    border-top-right-radius:12px; 
    border-top-left-radius:12px;

} 
QPushButton#Advance_disabled[Test=true]
{
    color:#808080; 
    background-color:#000000; 
    border-top-right-radius:12px; 
    border-top-left-radius:12px;
}

QPushButton#enabled[Test=true] 
{
    color:#000000; 
    background-color:#35BEF4; 
    font-weight:bold; 
    border-radius:10px;
}

QPushButton#enabled:hover
{
    color:#ffffff; 
    background-color:#054A73; 
    font-size:13px;
    font-weight:bold; 
    border: 1.5px solid #ffffff;
}
QPushButton#enabled:pressed
{
    color:#ffffff; 
    background-color:#000000; 
    border-radius:10px;
    border: 2px solid #000000;
}
/* button pressed hover color change as follow --------> QPushButton:hover:!pressed */
    
QPushButton#disabled[Test=true] 
{
    color:#000000; 
    background-color:#808080; 
    border-radius:10px;
}


/* ********************** CONSTANT LABELS ************************** */    
    
QLabel#DateTime
{
    color:#000000; 
    font-size:20px; 
    background-color:#3484A9;
}        

QLabel#Title
{
    background-color:#60000000; 
    border-radius:10px; 
    border: 0px solid #000000;
    /*box-shadow: 0px 0px 20px 10px #800000;*/
}

QLabel#sbg_l
{
    background-color:#60000000; 
    border-radius:10px; 
    border: 3px solid #000000;
}

QLabel#sbg_lx
{
    background-color:#3484A9; 
    border-radius:10px; 
    border: 2px solid #000000; 
    color:#808080; 
    font-weight:bold; 
    font-size:15px;
}

QLabel#sbg_lxx
{
    background-color:#000000; 
    border-top-left-radius:10px; 
    border-bottom-left-radius:10px; 
    border: 2px solid #000000; 
    color:#808080; 
    font-weight:bold; 
    font-size:15px;
}

QLabel#x_bottom
{
    background-color:#50000000; 
    border-bottom-right-radius:5px; 
    border-bottom-left-radius:10px;
}

QLabel#sbg_r
{
    background-color:#60000000; 
    border-radius:10px; 
    border: 3px solid #000000;
}

QLabel#sbg_r1
{
    background-color:#000000; 
    border-radius:10px; 
    border: 2px solid #000000; 
    color:#808080; 
    font-weight:bold; 
    font-size:25px;
}

QLabel#sbg_r2
{       
    background-color:#50000000; 
    border-radius:10px; 
    border: 3px solid #000000; 
    color:#808080; 
    font-weight:bold; 
    font-size:25px;        
}

QLabel#copyright
{
    color:#808080; 
    font-size:12px; 
    font-weight:bold; 
    padding-left:720px; 
    background-color:#000000;
}

/* ********************** PREDICTION LABELS **************************/
   
QLabel#predictionLabels
{
    color:#000000; 
    font-size:20px; 
    font-weight:bold; 
    background-color:#3484A9;
}

QLabel#predictionLabels_X
{
    color:#000000; 
    font-size:20px; 
    background-color:#3484A9;
}

QLabel#prediction5
{
    color:#A0A0A0; 
    font-size:18px; 
    font-weight:bold;
}

"""

# Defining style sheet here for train window.
#------------------------------------------------------------------------------

styleSheetTrain = """

/* ********************** CONSTANT LABELS ************************** */    
    
QLabel#sub_bg
{
    background-color:#40000000;
    border-radius:10px; 
    border: 2px solid #000000;
}   

QLabel#sub_title
{
    background-color:#40000000;
    border-radius:10px; 
    border: 0px solid #000000;
}
QLabel#textDisplay
{
    color:#000000; 
    font-size:20px; 
    font-weight:bold; 
    padding-left:8px;
    background-color:#3484A9;
    border-top-right-radius:10px; 
    border-bottom-right-radius:10px;
    border: 2px solid #000000;
}
QLabel#textDisplay1
{
    color:#000000; 
    font-size:20px;  
    padding-left:10px;
    background-color:#3484A9;
    border-top-right-radius:10px; 
    border-bottom-right-radius:10px;
    border: 2px solid #000000;
}
QLabel#textDisplayBg
{
    background-color:#000000;
    color:#808080;
    font-size:15px; 
    border-radius:10px;
    padding-left:15px
}
QLabel#textDisSetFreq
{
    background-color:#80000000;
    border: 3px solid #000000;
}
QLabel#textDisplayRecord
{
    background-color:#80000000;
    color:#808080;
    font-size:15px; 
    border: 3px solid #000000;   
}
QLabel#textDisplayRecordHeader
{
    color:#3484A9;
    font-size:25px;
    font-weight:bold;
    text-decoration: underline;
    font-family:Tahoma, Geneva, sans-serif;          
}
QLineEdit#classNameBox
{
    color:#000000; 
    background-color:#3484A9; 
    font-size:19px; 
    font-weight:bold;
    padding-left:15px;
    border: 2px solid #000000;
    border-top-right-radius:10px; 
    border-bottom-right-radius:10px;
}

/* **************************** BUTTONS **************************** */

QPushButton#restButtonTrain
{
    color:#808080; 
    background-color:#000000; 
    font-weight:bold; 
    border-radius:10px;
}
QPushButton#restButtonTrain:hover
{
    color:#ffffff; 
    background-color:#000000;
    font-size:12px;
    font-weight:bold; 
    border-radius:10px;
} 

    
"""

# Defining style sheet here for advance setting window.
#------------------------------------------------------------------------------

styleSheetAdvanceSetting = """

/* **************************** BUTTONS **************************** */

QPushButton#enabledAdvance 
{
    color:#808080; 
    background-color:#000000; 
    font-weight:bold;
    border-bottom-left-radius:0px; 
    border-bottom-right-radius:5px; 
    border-top-left-radius:0px;
    border-top-right-radius:5px;
}

QPushButton#enabledAdvance:hover
{
    color:#000000;
    font-size:15px;
    background-color:#0D86B1;
    font-weight:bold;
    font-family:"Arial Black", Gadget, sans-serif;
    border-bottom-left-radius:0px; 
    border-bottom-right-radius:5px; 
    border-top-left-radius:0px;
    border-top-right-radius:5px;
}
QPushButton#enabledAdvance:pressed
{
    color:#ffffff; 
    background-color:#000000; 
    border-bottom-left-radius:0px; 
    border-bottom-right-radius:5px; 
    border-top-left-radius:0px;
    border-top-right-radius:5px;
}

    
"""

# Defining style sheet here for notification window.
#------------------------------------------------------------------------------

styleSheetNotification = """

/* **************************** BUTTONS **************************** */

QPushButton#enabledNoti
{
    color:#808080; 
    background-color:#000000; 
    font-weight:bold; 
    border-radius:10px; 
}

QPushButton#enabledNoti:hover
{
    color:#000000;
    font-size:15px;
    font-family:"Arial Black", Gadget, sans-serif;
    background-color:#35BEF4;
    border: 1.5px solid #000000;
    font-weight:bold; 
    border-radius:10px; 
}
QPushButton#enabledNoti:pressed
{
    color:#ffffff; 
    background-color:#000000; 
    border-radius:10px; 
}

    
"""

# Defining style sheet here for dummy recording window.
#------------------------------------------------------------------------------

styleSheetDummy = """

/* **************************** BUTTONS **************************** */

QPushButton#enabledDummy
{
    color:#808080; 
    background-color:#000000; 
    font-weight:bold; 
    border-radius:10px; 

}

QPushButton#enabledDummy:hover
{
    color:#000000;
    font-size:14px;
    font-family:"Arial Black", Gadget, sans-serif;
    background-color:#35BEF4;
    border: 2.5px solid #000000;

    font-weight:bold; 
    border-radius:10px; 
}
QPushButton#enabledDummy:pressed
{
    color:#ffffff; 
    background-color:#000000; 
    border-radius:10px; 
}
    
"""
