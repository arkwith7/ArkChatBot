# ArkChatBot
웹기반 챗봇 어플리케이션을 만들수 있게 가이드하는 ChatBot Framework를 소개 합니다.
Python Django, JQuery, NLP(konlpy, Tensorflow)를 활용한 것으로,
아래의 설치가이드 설명 대로 수행 환경을 설정하고 이것을 응용한 자신만의 챗봇을 만들어 보시기 바랍니다. 


## 1. Anaconda 설치(Python 3.6 설치)
아나콘다 설치하기
https://repo.continuum.io/archive/ 에 접속 후 시스템환경에 맞는 버전의 Anaconda3을 다운로드합니다.
Anaconda3-5.0.0-Windows-x86_64.exe	510.0M	2017-09-26 14:14:53	fee3fad608d0006afa5c7bca4de3d02b
CMD(Windows Comand)에서 Python 버전을 확인 해보자.
```
C:\Users\saint\ChatBot>python --version
Python 3.6.2 :: Anaconda, Inc.
```

## 2. Git설치
### 2.1 Git SCM에 접속하여 설치 파일 다운로드
https://git-scm.com/

### 2.2 CMD(Windows Comand)에서 깃 버전을 확인 해보자.
```
C:\Users\saint\ChatBot>git --version
git version 2.28.0.windows.1
```

### 2.3 사용자 등록
```
C:\Users\saint\ChatBot>git config --global user.name "arkwith7"
```
```
C:\Users\saint\ChatBot>git config --global user.email "arkwith7@gmail.com"
```

### 2.4 확인
```
C:\Users\saint\ChatBot>git config --list
diff.astextplain.textconv=astextplain
filter.lfs.clean=git-lfs clean -- %f
filter.lfs.smudge=git-lfs smudge -- %f
filter.lfs.process=git-lfs filter-process
filter.lfs.required=true
http.sslbackend=openssl
http.sslcainfo=C:/Program Files/Git/mingw64/ssl/certs/ca-bundle.crt
core.autocrlf=true
core.fscache=true
core.symlinks=false
pull.rebase=false
credential.helper=manager
user.name=arkwith7
user.email=arkwith7@gmail.com
```

## 3. Java 설치
### 3.1 자바 JDK를 설치합니다.  여기에선1.8을 설치했습니다. 
https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html 
### 3.2 시스템에서 JAVA_HOME을 설정합니다. 
윈도우 키 + R을 누른 후,  sysdm.cpl를 실행합니다. 
고급탭에서 환경변수 버튼을 클릭한 후, 
시스템 변수 항목에 있는 새로 만들기 버튼을 클릭합니다.
변수 이름 항목에 JAVA_HOME을 적고
변수 값 항목에 다음 경로를 입력합니다. 
 JAVA_HOME = C:\Program Files\Java\jdk1.8.0_231
### 3.3 시스템 변수 항목에서 변수 Path를 찾은 후, 더블 클릭하면 
패스 추가를 위한 창이 보입니다. 
새로 만들기를 클릭한 후, 다음 경로를 입력합니다. 
```
C:\Program Files\Java\jdk1.8.0_231\bin
```
### 3.4 CMD(Windows Comand)에서 자바 버전을 확인 해보자.
```
c:\Users\saint\ChatBot>java -version
java version "1.8.0_261"
Java(TM) SE Runtime Environment (build 1.8.0_261-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.261-b12, mixed mode)
```

## 4. Python 가상환경 생성
### 4.1. 가상환경을 설치할 디렉토리로 이동
```
C:\Users\"윈도우 로그인 사용자명">cd ChatBot
```
### 4.2. virtualenv 설치
파이썬 가상환경을 설치하기 위해 virtualenv이용 한다
```
C:\Users\"윈도우 로그인 사용자명"\ChatBot>virtualenv --version
'virtualenv'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는
배치 파일이 아닙니다.
```
이상과 같이 **virtualenv**가 설치되지 않았다면
```
C:\Users\"윈도우 로그인 사용자명"\ChatBot>pip install virtualenv
Collecting virtualenv
........
```
```
C:\Users\"윈도우 로그인 사용자명"\ChatBot>virtualenv --version
virtualenv 20.0.31 from c:\users\saint\anaconda3\lib\site-packages\virtualenv\__init__.py
```
### 4.3. chat_env 가상환경 생성
```
C:\Users\"윈도우 로그인 사용자명"\ChatBot>virtualenv chat_env
.......
```
### 4.4. conda명령어로 chat_env 가상환경 생성
```
C:\Users\"윈도우 로그인 사용자명"\ChatBot>conda create -n chat_env python=3.6
```
생성한 가상환경을 활성화 한다
```
C:\Users\"윈도우 로그인 사용자명"\ChatBot>activate chat_env

(chat_env) C:\Users\"윈도우 로그인 사용자명"\ChatBot>

```
생성한 가상환경에서 빠져 나간다.
```
(chat_env) C:\Users\"윈도우 로그인 사용자명"\ChatBot>deactivate

C:\Users\"윈도우 로그인 사용자명"\ChatBot>

```
아나콘다 **conda** 명령어로 생성된 가상환경 목록을 조회한다. 
```
C:\Users\"윈도우 로그인 사용자명"\ChatBot>conda info --envs
# conda environments:
#
chat_env                 C:\Users\saint\Anaconda3\envs\chat_env
root                  *  C:\Users\saint\Anaconda3
```
가상환경을 제거 할 경우에는 
conda remove --name chat_env --all

## 5. TensorFlow 설치
주의 : 최신버전이 아니라 자신의 컴퓨터 환경에 맞는 버젼을 설치하는것이 중요함
- 본인의 GPU 사양 확인하기 > Compute Capability 확인(Compute Capability 3.5 이상의 NVIDIA® GPU 카드만 지원)
- Tensorflow 1.x 버전에서는 GPU를 사용하려면 CUDA 10.0을 지원, Tensorflow 2.x 버전에서는 10.1

OS: Windows 10
그래픽카드: NVIDIA GeForce GTX 1050
### 5.1. 텐서플로우(TensorFlow) 설치
설치가이드 : https://teddylee777.github.io/colab/tensorflow-gpu-install-windows
pip 명령어를 통해 텐서플로우를 설치합니다.
TensorFlow 1.x 버전 설치
```
pip install tensorflow==1.14.0
#pip install tensorflow-gpu==1.15.0
```

### 5.2. NVIDIA GPU 드라이버 설치
NVIDIA GPU 드라이버 설치 링크 : https://www.nvidia.com/download/index.aspx?lang=kr

제품 유형, 시리즈, 계열: 자신의 그래픽 카드 정보를 선택합니다.
운영체제: Windows 10을 선택하며, bit는 32/64 중 자신의 os와 일치된 bit 운영체제를 선택합니다.
다운로드 타입: Game Ready 드라이버 혹은 Studio 드라이버를 선택합니다. (큰 상관 없습니다)
선택이 완료 되었다면, 검색을 클릭합니다.

TensorFlow GPU 설치를 위해서는 418.x 버전 이상이 요구됩니다.
다운로드 받은 exe 파일을 실행하여 설치 합니다.

Window + R을 누르고 “cmd” 타입 후 터미널로 진입합니다.
터미널에 명령어 입력
nvidia-smi
명령어를 입력하여, 정상적으로 NVidia 그래픽 드라이버가 설치 되었는지 확인합니다.
```
C:\Users\saint\ChatBot>nvidia-smi
Thu Sep 03 15:59:32 2020
+----------------------------------------------------------------------------------+
| NVIDIA-SMI 452.06       Driver Version: 452.06       CUDA Version: 11.0          |
|----------------------+---------------------------+-------------------------------+
| GPU  Name          TCC/WDDM | Bus-Id      Disp.A | Volatile  Uncorr.         ECC |
| Fan Temp Perf  Pwr:Usage/Cap|       Memory-Usage | GPU-Util  Compute M.          |
|=============================+====================+===============================|
| 0  GeForce GTX 1050   WDDM  |00000000:01:00.0 Off|                           N/A |
| N/A   36C    P8  N/A /  N/A |   75MiB /  4096MiB |       0%              Default |
+-----------------------------+--------------------+-------------------------------+

+----------------------------------------------------------------------------------+
| Processes:                                                                       |
|  GPU   GI   CI        PID   Type   Process name                       GPU Memory |
|   ID   ID                                                         Usage          |
|==================================================================================|
|  No running processes found                                                      |
+----------------------------------------------------------------------------------+
```
### 5.3. CUDA Toolkit 다운로드 및 설치
CUDA Toolkit 다운로드 링크 : https://developer.nvidia.com/cuda-toolkit-archive
위 링크에서 자신이 맞는 버전의 CUDA Toolkit을 다운로드 합니다.
TensorFlow1.x 는 CUDA 10.0을 지원합니다. 따라서, CUDA 10. 0의 CUDA Toolkit 을 다운로드 받아 줍니다.

### 5.4. cuDNN SDK 설치
cuDNN SDK 다운로드 링크 : https://developer.nvidia.com/cudnn
Download cuDNN을 눌러 Download 받습니다.
멤버십이 요구 되므로, 회원가입을 안하신 분들은 회원가입 후 로그인을 진행합니다.

자신이 설치한 CUDA 버전에 맞는 cuDNN을 선택하여 다운로드 합니다.
Download cuDNN v7.6.5 (November 5th, 2019), for CUDA 10.0
cuDNN Library for Windows 10

### 5.5 환경 변수에서 CUDA_PATH 확인
(기본 C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0)

CUDA toolkit 버전에 맞는 cuDNN 라이브러리 다운로드 및 압축풀기 (Download cuDNN v7.6.2 (July 22, 2019), for CUDA 10.0)
https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.6.2.24/prod/10.0_20190719/cudnn-10.0-windows10-x64-v7.6.2.24.zip
압축 해제 3개의 파일을 앞선 CUDA_PATH 경로 내의 동일한 폴더로 이동

환경 변수 설정을 위해 "시스템 환경 변수 편집"으로 들어가줍니다.
path를 누르고 편집을 누릅니다.
```
    SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin;%PATH%
    SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\extras\CUPTI\libx64;%PATH%
    SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\include;%PATH%
```

### 5.6 설치 확인
```
C:\Users\saint\ChatBot>python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
2020-09-03 16:02:38.158098: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_100.dll
Tensor("Sum:0", shape=(), dtype=float32)
```

## 6. KoNLpy 설치 
### 6.1 JDK 설치여부 확인
우선 JDK를 1.7 버전 이상으로 설치해야 합니다.
```
C:\Users\saint\ChatBot>java -version
java version "1.8.0_261"
Java(TM) SE Runtime Environment (build 1.8.0_261-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.261-b12, mixed mode)
```

### 6.2 JDK 환경 변수 확인
```
C:\Users\saint\ChatBot>echo %JAVA_HOME%
```
```
C:\Program Files\Java\jdk1.8.0_261
```

JAVA_HOME이 없다면 윈도우 환경 변수에 추가해야하기 때문입니다.

윈도우 10기준)
제어판 > 시스템 및 보안 > 시스템 > 고급 시스템 설정 > 고급 > 환경 변수
새로 만들기(N)...를 누르고 JAVA_HOME이라는 환경 변수를 만듭니다. 환경 변수의 값은 앞서 찾았던 jdk 설치 경로입니다.

### 6.3 JPype 설치
이제 JAVA와 Python을 연결해주는 역할을 하는 JPype를 설치해야 합니다.

설치 주소 : https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype

해당 링크에서 적절한 버전을 설치해야 하는데 cp27은 파이썬 2.7, cp36은 파이썬 3.6을 의미합니다. 우리는 파이썬 3.6을 사용하고 있으므로 cp36이라고 적힌 JPype를 설치해야 합니다.

또 사용하는 윈도우 O/S가 32비트인지, 64비트인지에 따라서 설치 JPype가 다른데, 윈도우 32비트를 사용하고 있다면 win32를, 윈도우 64비트를 사용하고 있다면 win_amd64를 설치해야 합니다.

저의 경우에는 파이썬 3.6, 윈도우 64비트를 사용 중이므로 JPype1?0.6.3?cp36?cp36m?win_amd64.whl를 다운로드하였습니다.

윈도우의 명령 프롬프트에서 해당 파일의 경로로 이동하여 pip install 파일이름을 수행해야 합니다. 예를 들어 저의 경우에는 이와 같이 수행해야 합니다.

```
pip install JPype1-0.7.1-cp36-cp36m-win_amd64.whl
```
이제 JPype의 설치가 완료되었다면, KoNLpy를 사용할 준비가 되었습니다.

### 6.4 Konlpy 설치
```
pip install konlpy
```

## 7. 주피터 노트북 설치
- 주피터 노트북을 가상환경에서도 이용 할 수 있도록 설치
### 7.1. 가상환경에서 jupyter notebook 설치
```
pip install ipykernel
(chat_env) C:\Users\saint\ChatBot>pip install ipykernel
Collecting ipykernel
 .....
```

### 7.2. jupyter notebook에 가상환경 kernel 추가
```
python -m ipykernel install --user --name chat_env --display-name "ChatApp_env"
(chat_env) C:\Users\saint\ChatBot>python -m ipykernel install --user --name chat_env --display-name "ChatApp_env"
Installed kernelspec chat_env in C:\Users\saint\AppData\Roaming\jupyter\kernels\chat_env
```

### 7.3. jupyter notebook실행 
```
(chat_env) C:\Users\saint\ChatBot>jupyter notebook
[I 17:12:01.042 NotebookApp] Writing notebook server cookie secret to C:\Users\saint\AppData\Roaming\jupyter\runtime\notebook_cookie_secret
.......
```

### 7.4. 브라우져에 활성화된 Jupyter에서 New --> ChatApp_env 선택하여 새로운 창 열고 아래 코드 입력으로 CUDA와 PyTorch정상 설치 여부 확인

```
import tensorflow as tf
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
```

```
결과===>
Tensor("Sum_1:0", shape=(), dtype=float32)
```

## 8. Chatting Application을 위한 Python Package 설치
### 8.1 pip로 필요 파이선 패키지 설치
```
pip install -r requirements.txt
```

```
C:\Users\saint\ChatBot>pip install -r requirements.txt
```

### 8.2 NLTK 설치하고 Data 다운로드
```
nltk.download()
```

C:\Users\"윈도우 로그인 사용자명"\ChatBot>python
```
C:\Users\saint\ChatBot>python
Python 3.6.2 |Anaconda, Inc.| (default, Sep 19 2017, 08:03:39) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import nltk
>>> nltk.download()
showing info https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml
True
```

### 7.3 NLTK Data 다운로드 디렉토리로 대화 grammars파일 복사
```
C:\Users\saint\AppData\Roaming\nltk_data
~\arkwithsite\chatapp\ArkChatFramework\ArkChat\ 디렉토리에 있는 travel_kr.fcfg 파일을 
C:\Users\saint\AppData\Roaming\nltk_data\grammars\ 디렉토리로 복사
```

## 8. 케라스 설치(생략)
### 8.1 Git으로 keras 설치 파일을 내여 받는다.
```
git clone https://github.com/fchollet/keras.git
```

```
(chat_env) C:\Users\saint\ChatBot>git clone https://github.com/fchollet/keras.git
Cloning into 'keras'...
remote: Enumerating objects: 33256, done.
remote: Total 33256 (delta 0), reused 0 (delta 0), pack-reused 33256 eceiving objects: 100% (33256/33256), 11.10 MiB | 5.44 MiB/s
Receiving objects: 100% (33256/33256), 13.16 MiB | 5.92 MiB/s, done.
Resolving deltas: 100% (24244/24244), done.
```

### 8.2 내려 받은 디렉토리로 이동하여 설치
```
cd keras
python setup.py install
```

```
(chat_env) C:\Users\saint\ChatBot>cd keras

(chat_env) C:\Users\saint\ChatBot\keras>python setup.py install
running install
running bdist_egg
running egg_info
creating Keras.egg-info
.......
```

### 8.3 tensorflow 1.15와 호환되게 하기위해 다운그레이드
```
(chat_env) C:\Users\saint\ChatBot>cd ..
(chat_env) C:\Users\saint\ChatBot>pip install keras==2.2.5
Collecting keras==2.2.5
...........
```


## 9. Chat App 실행
Django웹 프로젝트인 arkwithsite로 이동하여 python manage.py runserver 실행
```
(chat_env) C:\Users\saint\ChatBot>cd arkwithsite

(chat_env) C:\Users\saint\ChatBot\arkwithsite>python manage.py runserver
```


### 9.1 오류발생시 조치 방법
? PyWinObject_FromULARGE_INTEGR @@ YAPEAU_object @@ AEBT_ULARGE_INTEGER @@@ Z 프로 시저의 진입 점은 동적 링크 라이브러리 <~ user> AppData \ Local \ Continuum \ anaconda3 \ envs \ test_env \ Library \ bin \ pythoncom36.dll에서 찾을 수 없습니다. .

-->
정확한 폴더 (<~ user> AppData \ Local \ Continuum \ anaconda3 \ envs \ test_env \ Library \ bin \ pythoncom37.dll.)에서 pythoncomXX.dll을 삭제했으며 동일한 문제가 발생하지 않았습니다
