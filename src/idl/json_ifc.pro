pro json_ifc,application

if n_elements(application) eq 0 then application = 'ws'

file_root = application 

print,' '
print,'=============== application: ',application

par_txt = xop_ifc_read(xop_ifcfile(file_root),'parameters')
ifc_txt = xop_ifc_read(xop_ifcfile(file_root),'interface')
if par_txt(0) EQ '' or ifc_txt(0) EQ '' then message,'Error... '
par =  make_str(par_txt)
ifc = make_str(ifc_txt)



;a = Xop_Input_Load(inputFile = application+'.xop')
a = par
;help,/str,a
json = JSON_SERIALIZE(a)
;acopy = JSON_PARSE(json, /TOARRAY, /TOSTRUCT)
;HELP, acopy,/str
openw,unit,application+'.json',/get_lun
printf,unit,json
free_lun,unit
print,'File written to disk: '+application+'.json'

names = tag_names(par)
flags = ifc.flags
help,flags,names
for i=0,n_elements(flags)-1 do begin
  ;print,flags[i],' <-- ',names[i]
  if strcompress(flags[i]) EQ '1' then begin
    flags[i] = 'True'
  endif else begin
    line = strupcase(flags[i])
    line = strsubstitute(line,'EQ',' == ')
    line = strsubstitute(line,'GE',' >= ')
    line = strsubstitute(line,'LE',' <= ')
    line = strsubstitute(line,'GT',' > ')
    line = strsubstitute(line,'LT',' < ')
    line = strsubstitute(line,'AND',' & ')
    line = strsubstitute(line,'NE',' != ')
    for k=0,n_elements(flags)-1 do begin
       line = strsubstitute(line,'W('+strcompress(k,/remove_all)+')','self.'+names[k])
    endfor
    flags[i] = line
  endelse
endfor

openw,unit,application+'.json.ext',/get_lun
printf,unit,vect2string(ifc.titles,/NoCompress)
printf,unit,vect2string(flags,/NoCompress)
printf,unit,vect2string(tag_names(par))
printf,unit,vect2string(ifc.flags,/NoCompress)
free_lun,unit
;print,'titles: ',ifc.titles
;print,'flags: ',ifc.flags
print,'File written to disk: '+application+'.json.ext'

end
