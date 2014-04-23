application = 'ws'
a = Xop_Input_Load(inputFile = application+'.xop')
help,/str,a
json = JSON_SERIALIZE(a)
acopy = JSON_PARSE(json, /TOARRAY, /TOSTRUCT)
HELP, acopy,/str
openw,unit,application+'.json',/get_lun
printf,unit,json
free_lun,unit
print,'File written to disk: '+application+'.json'
end
