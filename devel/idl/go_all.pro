;===============================================================================
;
; applications in xop_ifc
; 
;===============================================================================

openw,unit,'go_all.txt',/get_lun

; ATTENTION: 
; .compile xop_ifc

list  =  [ $
'black_body', $
'bm', $
'mlayer', $
'nsources', $
'ws', $
;'xpowder_fml', $
'xtubes', $
'xtube_w' ] 

for i=0,n_elements(list)-1 do begin
  print,'Calling ifc_json with application: ',list[i]
  printf,unit,list[i]
  json_ifc,list[i]
endfor


;===============================================================================
;
; applications in xop_defaults containing titles and flags
; 
;===============================================================================

;
; 
list  =  [ $
'xinpro', $
'xcrystal', $
'xwiggler', $
'xxcom']

for i=0,n_elements(list)-1 do begin
  print,'Calling ifc_xop_defaults with application: ',list[i]
  printf,unit,list[i]
  json_xop_defaults,list[i]
endfor

;===============================================================================
;
; applications in xop_ifc NOT containing titles and flags
; 
;===============================================================================

; now those entries that do not contain flags and titles

list  =  [ $
'xbfield', $
'xfilter', $
'xtc', $
'xus', $
'xurgent', $
'xyaup']

for i=0,n_elements(list)-1 do begin
  print,'Calling ifc_xop_defaults with application: ',list[i]
  printf,unit,list[i]
  json_xop_defaults,list[i],/noinfo
endfor

;===============================================================================
;
; applications in dabax_defaults containing titles and flags
; 
;===============================================================================

list  =  [ $
'xf0', $
'xcrosssec', $
'xf1f2', $
'xfh', $
;'crl', $
'mare']

for i=0,n_elements(list)-1 do begin
  print,'Calling ifc_xop_defaults,/dabax with application: ',list[i]
  printf,unit,list[i]
  json_xop_defaults,list[i],/dabax
endfor


;===============================================================================
;
; applications in xsh_defaults_preprocessors containing titles and flags
; 
;===============================================================================

; this section was used but the files mofidied by hand.
; commented to avoid overwriting
;list  =  [ $
;'xsh_bragg', $ 
;'xsh_pre_mlayer', $
;'xsh_prerefl', $
;'xsh_conic']
;
;for i=0,n_elements(list)-1 do begin
;  print,'Calling xsh_defaults_preprocessors,/xsh_preprocessors with application: ',list[i]
;  printf,unit,list[i]
;  json_xop_defaults,list[i],/xsh_preprocessors
;endfor


free_lun,unit
print,'File written to disk: go_all.txt'

end

