import pandas as pd
import numpy as np

important_words =['.','.>','2002', 'the', 'from', 'with', '.Received:', '+0100', 'a', 'for',
 'id', 'by', 'ESMTP', 'Linux', 'you', 'to', '[127.0.0.1]', 'I', 'it', '-0000', 'Microsoft',
 'my', 'that', 'have', '[127.0.0.1])', 'localhost', 'on', 'SMTP', 'be', '(Postfix)', '(localhost', '.Delivered-To:', '(single-drop);',
 '(fetchmail-5.9.0)', 'IMAP', 'phobos', '(IST)', '(8.11.6/8.11.6)', 'dogma.slashnull.org', '.X-Priority:', '7bit', '.Content-Transfer-Encoding:',
 '.Content-Type:', 'text/plain;', '1.0', '.MIME-Version:', '.Date:', '.Errors-To:', 'will', 'of', '.X-Beenthere:', '.X-Mailman-Version:',
 'bulk', '.List-Id:', '.Precedence:', '.Sender:', 'and', 'your', 'can', 'or', '--', '<jm@localhost>;', 'jalapeno', 'jm@localhost', '(jalapeno',
 'this', 'but', '#1', '-0700', 'than', 'was', 'email', 'fork-admin@xent.com', 'xent.com', '(PDT)', 'his', 'e-mail', 'had', '.Reply-To:', 'our', '<a',
 '.<table', 'We', '/>', '.<td', 'Helvetica']

important_domains = ['2ubh.com', 'Flashmail.com', 'No_important', 'SMTP1.ADMANMAIL.COM',
       'aol.com', 'btamail.net.cn', 'caramail.com', 'comcast.net',
       'dogma.slashnull.org', 'eudoramail.com', 'example.com',
       'excite.com', 'freshrpms.net', 'hotmail.com', 'insiq.us',
       'insurancemail.net', 'jmason.org', 'linux.ie',
       'lists.sourceforge.net', 'mail.com', 'msn.com', 'pathname.com',
       'perl.org', 'petting-zoo.net', 'python.org', 'redhat.com',
       'returns.groups.yahoo.com', 'securityfocus.com',
       'spamassassin.taint.org', 'srv0.ems.ed.ac.uk', 'taint.org',
       'unknown', 'xent.com', 'yahoo.com']

def replace(df):
    df["Message"] = df["Message"].str.replace(pat=r"[,\n]", repl=" ", regex=True)
    return df

def extract_domain(df, splitted=False):
    if not splitted:
        replace(df)
        df["s_Message"] = df["Message"].str.split(" ")

    df["email"] =  df["s_Message"].apply(lambda x: x[np.argmax(np.char.lower(np.array(x)) == "from") + 1])
    return df

def introductory_pipeline(df, important_words=important_words,important_domains=important_domains):
    df = extract_domain(df)
    df["domain"] = df["email"].str.split("@").str[1]
    df.drop("email", axis=1, inplace=True)

    df["Message"] = df["s_Message"]
    df.drop("s_Message", axis=1, inplace=True)

    word_counts = [0 for i in range(df.shape[0])]
    counter = 0
    for index, row in df.iterrows():
        x = pd.Series(row["Message"])
        x = x[x != ""]
        x = x.value_counts().to_dict()
    
        table = np.zeros(len(important_words), dtype=np.int16)
    
        for index in range(len(important_words)):
            count = x.get(important_words[index], 0)
            table[index] = count
        
        word_counts[counter] = table
        counter += 1

    counted_words = pd.concat(
        [
            pd.DataFrame(word_counts, columns=important_words), 
            df.drop("Message",axis=1).reset_index(drop=True)
        ], 
        axis=1
    )
    
    important_domains = pd.DataFrame(important_domains, columns=["domain"])
    important_domains["pointer"] = 1

    counted_words.loc[counted_words["domain"].isna(), "domain"] = "unknown"
    counted_words = counted_words.merge(important_domains, how="left", on="domain")
    counted_words.loc[counted_words["pointer"].isna(), "domain"] = "unimportant"
    counted_words.drop("pointer", axis=1, inplace=True)

    return counted_words
    
    
    

    