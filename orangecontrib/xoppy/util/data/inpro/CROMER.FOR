	implicit real*8 (a-h,o-z)
	external sigma0, sigma1, sigma2, sigma3, lgndr
	dimension xk(10), xr(10), fp(10,24), fpp(10,24), abs(10,24)
	dimension ew(14), sig(14), el(14), sl(14)
	dimension m1(14), m2(14), m3(14)
	dimension cxb(10), sumfp(10), sumfpp(10)
	dimension t(32)
	dimension xjensn(10),et(10)
	dimension eg(5)
	dimension eterm(98),wt(98),norb(98)
	common /gaus/ cx, bb, sigg(5), rx, icount
	common /plt/ nplotl, nat, nshel(3,24)
	common /edge/ sedge
	data eterm/0.0D0,.0D0,.001D0,.001D0,.002D0,.003D0,.005D0,.007D0
	1,.009D0,
	1.011D0,.014D0,.018D0,.021D0,.026D0,.030D0,.035D0,.041D0,.047D0,
	2.053D0,.060D0,.068D0,.075D0,.084D0,.093D0,.102D0,.113D0,.123D0,
	3.135D0,.146D0,.159D0,.172D0,.186D0,.200D0,.215D0,.231D0,.247D0,
	4.264D0,.282D0,.300D0,.319D0,.338D0,.359D0,.380D0,.401D0,.424D0,
	5.447D0,.471D0,.496D0,.521D0,.547D0,.575D0,.602D0,.631D0,.660D0,
	6.690D0,.721D0,.753D0,.786D0,.819D0,.854D0,.889D0,.925D0,.962D0,
	71.0D0,1.039D0,1.079D0,1.119D0,1.161D0,1.204D0,1.248D0,1.293D0,
	81.338D0,1.385D0,1.433D0,1.482D0,1.532D0,1.583D0,1.636D0,1.689D0,
	91.743D0,1.799D0,1.856D0,1.914D0,1.973D0,2.033D0,2.095D0,2.157D0,
	12.221D0,2.287D0,2.353D0,2.421D0,2.490D0,2.561D0,2.633D0,2.707D0,
	22.782D0,2.858D0,2.936D0/
	data wt/1.0079D0,4.00260D0,6.941D0,9.01218D0,10.81D0,12.011D0,
	114.0067D0,15.9994D0,18.9984D0,20.179D0,22.98977D0,24.305D0,
	226.98154D0,28.0855D0,30.97376D0,32.06D0,35.453D0,39.948D0,
	339.0983D0,40.08D0,44.9559D0,47.88D0,50.9415D0,51.996D0,
	454.9380D0,55.847D0,58.9332D0,58.69D0,63.546D0,65.38D0,69.72D0,
	572.59D0,74.9216D0,78.96D0,79.904D0,83.80D0,85.4678D0,87.62D0,
	688.9059D0,91.22D0,92.9064D0,95.94D0,98.D0,101.07D0,102.9055D0,
	7106.42D0,107.868D0,112.41D0,114.82D0,118.69D0,121.75D0,
	9127.60D0,126.9045D0,131.29D0,132.9054D0,137.33D0,138.9055D0,
	8140.12D0,140.9077D0,144.24D0,145.D0,150.36D0,151.96D0,157.25D0,
	9158.9254D0,162.50D0,164.9304D0,167.26D0,168.9342D0,173.04D0,
	1174.67D0,178.49D0,180.9479D0,183.85D0,186.207D0,190.2D0,
	3192.22D0,195.08D0,196.9655D0,200.59D0,204.383D0,207.2D0,
	4208.9804D0,209.D0,210.D0,222.D0,223.D0,226.0254D0,227.0278D0,
	5232.0381D0,231.0359D0,238.0482D0,237.0482D0,239.D0,243.D0,247.D0,
	6247.D0,251.D0/
	data norb/0,0,2,2,3,3,4,4,4,4,4,4,5,6,7,7,7,7,7,7,7,
	17,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,12,12,13,13,14,14,14,14,14,
	214,14,14,14,14,14,14,14,17,17,17,18,18,18,18,18,18,19,19,19,19,19,
	319,19,19,20,20,20,21,21,21,21,21,22,22,23,23,24,24,24,24,24,24,24,
	424,24,24,24,24,24,24,24/
	data c/137.0367D0/
	data pi/3.14159265D0/
	data au/2.80022D+7/
	data c1/.02721D0/
	data xev/12397.639D0/
	mx=5
c
c
c**********  set input, output and x section files*****
	in=5
	io=7
	is=1
	OPEN(UNIT=1,NAME='RK2:CROMER.DAT',TYPE='OLD')
c**********
	WRITE(7,7000)
7000	FORMAT('$INPUT ATOMIC SYMBOL: ')
	read (in,230) natom
	write(7,7005)
7005	format('$INPUT ATOMIC #: ')
	read(in,235) iz
	no=norb(iz)
	WRITE(7,7010)
7010	FORMAT('$INPUT # OF WAVE AND ORDER: ')
	read (in,250) nw,nord
c
c
c*****read number of xray values to be interpolated,
c	 interpolation type, and iplot=0(no plot), iplot=1(plot xsections)
	do 10 k=1,nw
	WRITE(7,7020) k
7020	FORMAT('$INPUT X-RAY ENERGY (eV) #',i2,': ')
	read (in,270) xr(k)
	if(xr(k).lt.25.0) xr(k)=xev/xr(k)
	xk(k)=0.001*xr(k)
10	CONTINUE
	rewind is
	do 20 i=1,nw
	cxb(i)=0.0
	do 20 j=1,no
	fp(i,j)=0.0
	fpp(i,j)=0.0
20	CONTINUE
	do 160 j=1,no
	do 30 k=1,mx
21	read(is,280) nat,nj,nshel(1,j),nshel(2,j),NSHEL(2,J)
	1,xw,ew(k),sig(k)
c
c	nat=atomic symbol
c	nj=orbital sequence number
c	nshel=orbital type. 1s1/2 etc.
c	xw=energy in angstroms
c	ew=energy in kev
c	sig=cross section in barns
c	be=binding energy(kev)
c	if=0,1,2 function type
c
c*****read mx energies and x sections for orbital j
c
	if (nat.ne.natom) go to 21
	if (nj.ne.j) go to 220
30	CONTINUE
	do 40 k=1,5
	read (is,280) nat,nj,nshel(1,j),nshel(2,j),nshel(3,j)
	1,xw,eg(k),sigg(k),be,if
c*****read 5 energies and x sections for orbital j
c*****   for the gauss integration points. binding energy
c	  and function type also
	if (nat.ne.natom) go to 220
	if (nj.ne.j) go to 220
	if (be.le.0.) go to 220
	ew(k+mx)=eg(k)
	sig(k+mx)=sigg(k)
40	CONTINUE
	nx=mx+5
	if (if.ne.0) go to 50
	nx=nx+1
c***** if=0 so read x sextion at energy=1.001*binding energy
	read (is,280) nat,nj,nshel(1,j),nshel(2,j),nshel(3,j)
	1,xw,ew(nx),sig(nx)
	if (nat.ne.natom) go to 220
	edg=ew(nx)
	sigedg=sig(nx)
50	CONTINUE
	bb=be/c1
	do 60 i=1,5
	sigg(i)=sigg(i)/au
60	CONTINUE
c*****sort all x sections
	call sort(nx,ew,sig)
c*****sort the five cross sections at integration points
	call sort(5,eg,sigg)
c*****change to logs for interpolation
	do 70 k=1,nx
	el(k)=0.
	sl(k)=0.
c
	el(k)=dlog(ew(k))
c
	if (sig(k).eq.0.0) go to 70
c
	sl(k)=dlog(sig(k))
c
70	CONTINUE
	do 150 k=1,nw
	mf=0
c
c
	zx=dlog(xk(k))
c
c*****zx=log of xray(kev) energy
	cx=0.
	if (be.gt.xk(k)) go to 120
	if (nord.ne.0) go to 80
	call xsect (zx,el,sl,cx,nx)
	go to 110
80	do 90 m=1,nx
	n1=m
	if (sl(m).ne.0.0) go to 100
90	continue
100	mm=nx-n1+1
	cx=aknint(zx,mm,nord,el(n1),sl(n1),t)
c
	cx=dexp(cx)
c
c*****cx is the interpolated x section in barns
110	cxb(k)=cxb(k)+cx
c	*****cxb is sum to get mu/rho
c*****change cx to atomic units
	cx=cx/au
120	icount=6
c*****rx=xray energy in atomic units
	rx=xk(k)/c1
	if (if.ne.0) go to 130
	if (be.lt.xk(k)) go to 130
c*****sedge is xsection in atomic units at energy=1.001*be
	sedge=sigedg/au
	cx=0.0
	fp(k,j)=gauss(1,sigma3,5,lgndr)*c/(2.0*pi**2)
	mf=3
	go to 140
130	continue
	if (if.eq.0) fp(k,j)=gauss(1,sigma0,5,lgndr)*c/(2.0*pi**2)
	if (if.eq.1) fp(k,j)=gauss(1,sigma1,5,lgndr)*c/(2.0*pi**2)
	if (if.eq.2) fp(k,j)=gauss(1,sigma2,5,lgndr)*c/(2.0*pi**2)
140	continue
	fpp(k,j)=0.
	if (cx.ne.0.0) fpp(k,j)=c*cx*rx/(4.0*pi)
	corr=0.0
c
	if (cx.ne.0.0) corr=-cx*rx*0.5*dlog((rx+bb)/(rx-bb))*c/(2.0*pi**2)
	if (mf.eq.3) corr=0.5*sedge*bb**2*dlog((-bb+rx)/(-bb-rx))/rx*c/(2.
	1 *pi**2)
c
	fp(k,j)=fp(k,j)+corr
	abs(k,j)=cx*au
150	continue
c
c
160	continue
	write (io,290) natom,iz,no,wt(iz),eterm(iz)
	write (io,240) nw,nord
	write (io,260) (xr(i),i=1,nw)
	write (io,300)
	do 170 i=1,nw
	sumfp(i)=0.0
	sumfpp(i)=0.
170	CONTINUE
	do 180 j=1,no
	write (io,310) (nshel(1,j),nshel(2,j),nshel(3,j),
	1(fp(k,j),k=1,nw))
	do 180 k=1,nw
	sumfp(k)=sumfp(k)+fp(k,j)
180	CONTINUE
	write (io,300)
	write (io,322) (sumfp(k),k=1,nw)
	do 185 k=1,nw
	xjensn(k)=-0.5*float(iz)*(xk(k)/c1/137.0367**2)**2
185	CONTINUE
	do 186 k=1,nw
186	et(k)=-eterm(iz)
	write (io,323)(et(k),k=1,nw)
	write (io,321)(xjensn(k),k=1,nw)
	do 189 k=1,nw
189	sumfp(k)=sumfp(k)+et(k)+xjensn(k)
	write (io,300)
	write (io,320)(sumfp(k),k=1,nw)
	write (io,300)
	do 190 j=1,no
	write (io,310) (nshel(1,j),nshel(2,j),nshel(3,j),
	1(fpp(k,j),k=1,nw))
	do 190 k=1,nw
	sumfpp(k)=sumfpp(k)+fpp(k,j)
190	continue
	write (io,300)
	write (io,330) (sumfpp(k),k=1,nw)
	do 200 k=1,nw
	cxb(k)=cxb(k)*0.602472/wt(iz)
200	continue
	write (io,340) (cxb(k),k=1,nw)
	write (io,300)
	write (io,350)
	do 210 j=1,no
	write (io,360) (nshel(1,j),nshel(2,j),nshel(3,j),
	1(abs(k,j),k=1,nw))
210	CONTINUE
c
c
	stop
220	write(io,370)
	stop
c
230	format (a2)
235	format(i5)
240	format (' NW=',i5,'  NORD=',i5)
250	format (3i5)
260	format (' ENERGY ',10f10.2)
270	format (10f10.2)
280	format (a2,2X,i4,3a2,1p3e15.8,e15.8,i2)
290	format (3x,a2,2i5,2f8.3)
300	format (1h )
310	format (2x,3a2,10f10.3)
320	format ('     FP=',10f10.3)
321	format (' JENSEN=',10f10.3)
322	format ('   P.E.=',10f10.3)
323	format ('  ETERM=',10f10.3)
330	format ('    FPP=',10f10.3)
340	format (' MU/RHO=',10f10.1)
350	format (15x,'CROSS SECTION(BARNS) AT XRAY ENERGY',/)
360	format (2x,3a2,1p10e10.3)
370	format (' DATA FILE ERROR')
	end
c
c
	subroutine xsect (zx,el,sl,cx,nx)
	implicit real*8 (a-h,o-z)
	dimension el(14), sl(14)
c*****find el(k) closest to zx
	er=1000000.
	do 10 l=1,nx
c
	p=dabs(zx-el(l))
c
	if (p.gt.er) go to 10
	er=p
	ll=l
   10 continue
	ll=ll-1
	if (ll.eq.0) ll=1
	if (ll.eq.12) ll=11
	if (sl(ll).eq.0.) ll=ll+1
	det=el(ll+2)**2*(el(ll+1)-el(ll))+el(ll+1)**2*(el(ll)-el(ll+2))+el
	1 (ll)**2*(el(ll+2)-el(ll+1))
	a0=(el(ll)**2*(sl(ll+1)*el(ll+2)-sl(ll+2)*el(ll+1))+el(ll+1)**2*
	1 (sl(ll+2)*el(ll)-sl(ll)*el(ll+2))+el(ll+2)**2*(sl(ll)*el(ll+1)-sl
	2 (ll+1)*el(ll)))/det
	a1=(el(ll)**2*(sl(ll+2)-sl(ll+1))+el(ll+1)**2*(sl(ll)-sl(ll+2))+el
	1 (ll+2)**2*(sl(ll+1)-sl(ll)))/det
	a2=(sl(ll)*(el(ll+2)-el(ll+1))+sl(ll+1)*(el(ll)-el(ll+2))+sl(ll+2)
	1 *(el(ll+1)-el(ll)))/det
c
	cx=dexp(a0+a1*zx+a2*zx**2)
c
	return
	end
c***********************************************************************
c
	double precision function sigma0 (k,x)
	implicit real*8 (a-h,o-z)
	common /gaus/ cx, bb, sg(5), rx, icount
	icount=icount-1
	sigma0=sg(icount)*bb**3/x**2/(rx**2*x**2-bb**2)-bb*cx*rx**2/(rx**2
	1 *x**2-bb**2)
	return
	end
c***********************************************************************
c
	double precision function sigma1 (k,x)
	implicit real*8 (a-h,o-z)
	common /gaus/ cx, bb, sg(5), rx, icount
	icount=icount-1
c
	sigma1=0.5*bb**3*sg(icount)/(dsqrt(x)*(rx**2*x**2-bb**2*x))
c
	return
	end
c***********************************************************************
c
	double precision function sigma2 (k,x)
	implicit real*8 (a-h,o-z)
	common /gaus/ cx, bb, sg(5), rx, icount
	icount=icount-1
	denom=x**3*rx**2-bb**2/x
	sigma2=2.0*bb*sg(icount)*bb**2/x**4/denom-2.0*bb*cx*rx**2/denom
	return
	end
c***********************************************************************
	double precision function sigma3 (k,x)
	implicit real*8 (a-h,o-z)
	common /edge/ sedge
	common /gaus/ cx, bb, sg(5), rx, icount
	icount=icount-1
	sigma3=bb**3*(sg(icount)-sedge*x**2)/(x**2*(x**2*rx**2-bb**2))
	return
	end
c***********************************************************************
	subroutine lgndr (m,k,aa,z)
	implicit real*8 (a-h,o-z)
	dimension a(68), x(62)
	data x(1) /.06943184420297D0/
	data x(2) /.33000947820757D0/
	data x(3) /.04691007703067D0/
	data x(4) /.23076534494716D0/
	data x(5) /.03376524289992D0/
	data x(6) /.16939530676687D0/
	data x(7) /.38069040695840D0/
	data x(8) /.02544604382862D0/
	data x(9) /.12923440720030D0/
	data x(10) /.29707742431130D0/
	data x(11) /.01985507175123D0/
	data x(12) /.10166676129319D0/
	data x(13) /.23723379504184D0/
	data x(14) /.40828267875217D0/
	data x(15) /.01591988024619D0/
	data x(16) /.08198444633668D0/
	data x(17) /.19331428364971D0/
	data x(18) /.33787328829809D0/
	data x(19) /.01304673574141D0/
	data x(20) /.06746831665551D0/
	data x(21) /.16029521585049D0/
	data x(22) /.28330230293537D0/
	data x(23) /.42556283050918D0/
	data x(24) /.01088567092697D0/
	data x(25) /.05646870011595D0/
	data x(26) /.13492399721298D0/
	data x(27) /.24045193539659D0/
	data x(28) /.36522842202382D0/
	data x(29) /.00921968287664D0/
	data x(30) /.04794137181476D0/
	data x(31) /.11504866290285D0/
	data x(32) /.20634102285669D0/
	data x(33) /.31608425050091D0/
	data x(34) /.43738329574426D0/
	data x(35) /.00790847264071D0/
	data x(36) /.04120080038851D0/
	data x(37) /.09921095463335D0/
	data x(38) /.17882533027983D0/
	data x(39) /.27575362448178D0/
	data x(40) /.38477084202243D0/
	data x(41) /.00685809565159D0/
	data x(42) /.03578255816821D0/
	data x(43) /.08639934246512D0/
	data x(44) /.15635354759416D0/
	data x(45) /.24237568182092D0/
	data x(46) /.34044381553605D0/
	data x(47) /.44597252564632D0/
	data x(48) /.600374098758D-2/
	data x(49) /.31363303799647D-1/
	data x(50) /.75896708294787D-1/
	data x(51) /.13779113431991D0/
	data x(52) /.21451391369574D0/
	data x(53) /.30292432646121D0/
	data x(54) /.39940295300128D0/
	data x(55) /.00529953250417D0/
	data x(56) /.02771248846338D0/
	data x(57) /.06718439880608D0/
	data x(58) /.12229779582250D0/
	data x(59) /.19106187779868D0/
	data x(60) /.27099161117138D0/
	data x(61) /.35919822461038D0/
	data x(62) /.45249374508118D0/
	data a(1) /.17392742256873D0/
	data a(2) /.32607257743127D0/
	data a(3) /.11846344252810D0/
	data a(4) /.23931433524968D0/
	data a(5) /.28444444444444D0/
	data a(6) /.85662246189585D-1/
	data a(7) /.18038078652407D0/
	data a(8) /.23395696728635D0/
	data a(9) /.06474248308443D0/
	data a(10) /.13985269574464D0/
	data a(11) /.19091502525256D0/
	data a(12) /.20897959183674D0/
	data a(13) /.05061426814519D0/
	data a(14) /.11119051722669D0/
	data a(15) /.15685332293894D0/
	data a(16) /.18134189168918D0/
	data a(17) /.04063719418079D0/
	data a(18) /.09032408034743D0/
	data a(19) /.13030534820147D0/
	data a(20) /.15617353852000D0/
	data a(21) /.16511967750063D0/
	data a(23) /.07472567457529D0/
	data a(24) /.10954318125799D0/
	data a(25) /.13463335965500D0/
	data a(26) /.14776211235738D0/
	data a(27) /.02783428355809D0/
	data a(28) /.06279018473245D0/
	data a(29) /.09314510546387D0/
	data a(30) /.11659688229599D0/
	data a(31) /.13140227225512D0/
	data a(32) /.13646254338895D0/
	data a(33) /.02358766819326D0/
	data a(34) /.05346966299766D0/
	data a(35) /.08003916427167D0/
	data a(36) /.10158371336153D0/
	data a(37) /.11674626826918D0/
	data a(38) /.12457352290670D0/
	data a(39) /.02024200238266D0/
	data a(40) /.04606074991886D0/
	data a(41) /.06943675510989D0/
	data a(42) /.08907299038097D0/
	data a(43) /.10390802376845D0/
	data a(44) /.11314159013145D0/
	data a(45) /.11627577661544D0/
	data a(46) /.01755973016588D0/
	data a(47) /.04007904357988D0/
	data a(48) /.06075928534395D0/
	data a(49) /.07860158357910D0/
	data a(50) /.09276919873897D0/
	data a(51) /.10259923186065D0/
	data a(52) /.10763192673158D0/
	data a(53) /.01537662099806D0/
	data a(54) /.03518302374405D0/
	data a(55) /.05357961023359D0/
	data a(56) /.06978533896308D0/
	data a(57) /.08313460290850D0/
	data a(58) /.09308050000778D0/
	data a(59) /.09921574266356D0/
	data a(60) /.10128912096278D0/
	data a(61) /.01357622970588D0/
	data a(62) /.03112676196932D0/
	data a(63) /.04757925584125D0/
	data a(64) /.06231448562777D0/
	data a(65) /.07479799440829D0/
	data a(66) /.08457825969750D0/
	data a(67) /.09130170752246D0/
	data a(68) /.09472530522754D0/
	kk=k
	if ((m.gt.16).or.(m.lt.4)) kk=4
	is=0
	ih=(m+1)/2
	z=.5
	if (mod(m,2).eq.1) is=-1
	ip=kk
	t=0.
	if (ip.le.ih) go to 10
	ip=m+1-ip
	t=-1
   10 i4=m-4
	ia=(i4*(m+4)+is)/4+ip
	aa=a(ia)
	if ((ip.eq.ih).and.(is.lt.0)) return
	ia=ia-(i4+is)/2
	z=-t+dsign(x(ia),t)
	return
	end
c***********************************************************************
c
	double precision function gauss (n,y,m,ltbl)
	implicit real*8 (a-h,o-z)
	logical*1 cmt(47)
	dimension m(6),g(6),z(6)
	data cmt/'G','A','U','S','S',' ',' ',' ','N',' ','N','O',
	1'T',' ','I','N',' ','(','1',',','6',')','.',' ',' ','R',
	2'E','S','U','L','T','S',' ',' ',' ','S','E','T',' ','T',
	3'O',' ','Z','E','R','O','.'/
	dimension a(6)
	if ((n.gt.6).or.(n.lt.1)) go to 140
	nn=n
	go to (110,90,70,50,30,10), nn
   10 j=1
	g(6)=0.
   20 call ltbl (m(6),j,a(6),z(6))
   30 k=1
	g(5)=0.
   40 call ltbl (m(5),k,a(5),z(5))
   50 l=1
	g(4)=0.
   60 call ltbl (m(4),l,a(4),z(4))
   70 jj=1
	g(3)=0.
   80 call ltbl (m(3),jj,a(3),z(3))
   90 kk=1
	g(2)=0.
  100 call ltbl (m(2),kk,a(2),z(2))
  110 ll=1
	g(1)=0.
  120 call ltbl (m(1),ll,a(1),z(1))
	g(1)=g(1)+a(1)*y(1,z)
	ll=ll+1
	if (ll.le.m(1)) go to 120
	if (nn.eq.1) go to 130
	g(2)=g(2)+a(2)*y(2,z)*g(1)
	kk=kk+1
	if (kk.le.m(2)) go to 100
	if (nn.eq.2) go to 130
	g(3)=g(3)+a(3)*y(3,z)*g(2)
	jj=jj+1
	if (jj.le.m(3)) go to 80
	if (nn.eq.3) go to 130
	g(4)=g(4)+a(4)*y(4,z)*g(3)
	l=l+1
	if (l.le.m(4)) go to 60
	if (nn.eq.4) go to 130
	g(5)=g(5)+a(5)*y(5,z)*g(4)
	k=k+1
	if (k.le.m(5)) go to 40
	if (nn.eq.5) go to 130
	g(6)=g(6)+a(6)*y(6,z)*g(5)
	j=j+1
	if (j.le.m(6)) go to 20
  130 gauss=g(nn)
	return
  140 call labrt (1,cmt,1)
	gauss=0.
	return
	end
c***********************************************************************
	subroutine labrt (isw,lhol,inx)
	implicit real*8 (a-h,o-z)
	logical*1 lhol(46)
	logical ps, ts
	if ((isw.eq.0).or.(isw.gt.5)) return
	go to (10,20,30,40,50), isw
	data np /10/, ps /.true./, ts /.false./
   10 if (ps.and.(np.gt.0)) print 60, lhol,inx
	np=np-1
	if (ts) call exit
	return
   20 ps=.false.
	return
   30 ps=.true.
	np=inx
	return
   40 ts=.true.
	return
   50 ts=.false.
	return
   60 format (1h0,9x,46a1,3x,i6)
	end
	double precision function aknint (xbar,in,im,x,y,t)
	implicit real*8 (a-h,o-z)
c
c aitken repeated interpolation
c
c   xbar = abscissa at which interpolation is desired
c   iabs(in) = no. of values in table
c		  if in.gt.0, chk ordering of x(i).
c		  if in.lt.0, skip preceeding test.
c   im   = degree of approximating polynomial
c   x    = vector of iabs(in) values of abscissa
c   y    = vector of iabs(in) values of ordinate
c   t    = temporary storage vector of 4*(m+1) locations)
c
c
c
	double precision t, dxbar
	dimension t(80), x(9), y(9)
	dxbar=xbar
	n=iabs(in)
	m=im
	if (m.ge.n) go to 120
   10 k=n-1
	if (n.lt.2) go to 110
	s=x(2)-x(1)
	if (in.lt.0) go to 30
c chk if order monotonic
	if (n.eq.2) go to 30
	do 20 i=3,n
	z=(x(i)-x(i-1))*s
   20 if (z.le.0.) go to 100
   30 if (s.lt.0.) go to 50
c increasing order
	do 40 j=1,n
   40 if (xbar.le.x(j)) go to 70
	j=n
	go to 70
c decreasing order
   50 do 60 j=1,n
   60 if (xbar.ge.x(j)) go to 70
	j=n
   70 k=m
	m=m+1
	j=j-m/2
	j=max0(j,1)
	j=min0(j,n-k)
	mend=j+k
	do 80 i=j,mend
	kk=i-j+1
	t(kk)=y(i)
   80 t(kk+m)=x(i)-dxbar
	do 90 i=1,k
	kk=i+1
	do 90 jj=kk,m
	t(jj)=(t(i)*t(jj+m)-t(jj)*t(i+m))/(x(jj+j-1)-x(i+j-1))
   90 continue
	aknint=t(m)
	return
  100 print 4
    4 format (35h aknint x(i) not sequenced properly)
  110 print 3
    3 format (36h aknint n.lt.2 ybar returned as y(1))
	aknint=y(1)
	return
  120 print 1
    1 format (48h aknint warning order of interpolation too large)
	m=n-1
	go to 10
	end
	subroutine sort (n,a,b)
	implicit real*8 (a-h,o-z)
	dimension a(1),b(1)
	m=n-1
	do 200 i=1,m
	i1=i+1
	do 100 j=i1,n
	if(a(j).gt.a(i))go to 100
	x=a(j)
	y=a(i)
	a(i)=x
	a(j)=y
	x=b(j)
	y=b(i)
	b(i)=x
	b(j)=y
  100 continue
  200 continue
	return
	end
