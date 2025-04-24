import pandas as pd
import numpy as np

important_words =['by','.','with','2002','the','of','-0500','to','I','a',
                  'that','it','.>','is','+0100','.Received:','ESMTP','id',
                  'Linux','and','.Content-Type','.Sender:','.Errors-To:',
                  '.X-Mailman-Version:','.Precedence:','bulk', '.List-Id',
                  '.X-Beenthere', '(Postfix)', 'using', '.Delivered-To:',
                  'or', '<jm@localhost>;', '-0400', 'IMAP', '(fethmail-5.9.0)',
                  'jm@localhost','(single-drop);', '(IST)', 'you', '(PDT)', 
                  '-0700', '[127.0.0.1]', 'SMTP','(jalapeno','in',
                  '.Content-Transfer-Encoding:','will', 'your','email','Microsoft',
                  'its','>','our','want', '<a', '.<font']

important_domains = [
     'xent.com', 'jmason.org', 'linux.ie', 'lists.sourceforge.net',
     'freshrpms.net', 'unknown', 'redhat.com', 'hotmail.com', 'yahoo.com',
     'perl.org', 'returns.groups.yahoo.com', 'aol.com', 'msn.com',
     'insurancemail.net', 'taint.org', 'insiq.us', 'python.org',
     'petting-zoo.net', 'securityfocus.com', 'comcast.net', 'pobox.com',
     'btamail.net.cn', 'eudoramail.com']

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
    
    
    

    