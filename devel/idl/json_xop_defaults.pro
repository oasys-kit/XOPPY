pro json_xop_defaults,application, noinfo=noinfo, dabax=dabax, xsh_preprocessors=xsh_preprocessors

if n_elements(application) eq 0 then application = 'xinpro'

if keyword_set(xsh_preprocessors) then begin
    str = xsh_defaults_preprocessors(application)
endif else begin
    if keyword_set(dabax) then begin
        str = dabax_defaults(application)
    endif else begin
        str = xop_defaults(application)
    endelse
endelse

application = strlowcase(application) ; changed in xop_defaults...

print,' '
print,'=============== application: ',application

if keyword_set(noinfo) then begin
    par = str
    flags = replicate('1',n_tags(str))
    titles = replicate('Dummy_title',n_tags(str))
endif else begin
    par = str.parameters
    flags = str.flags
    titles = str.titles
endelse



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
help,flags,titles,names
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
printf,unit,vect2string(titles,/NoCompress)
printf,unit,vect2string(flags,/NoCompress)
printf,unit,vect2string(tag_names(par))
printf,unit,vect2string(flags,/NoCompress)
free_lun,unit
print,'File written to disk: '+application+'.json.ext'

end
