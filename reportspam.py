from flask import Flask
import MySQLdb
import time

DB="pdns"
USER="pdns"
PASSWORD="FIND_THIS_IN_ETC_POWERDNS_PDNS_D_MYSQL"
HOST="localhost"

DOMAIN=1
DOMAIN_NAME="bl.mydomain.com"

app = Flask(__name__)
app.config.update(DEBUG=True)

@app.route("/report/<ip>")
def report(ip):
    conn = MySQLdb.connect(HOST, USER, PASSWORD, DB)
    c = conn.cursor()
    reversedip = ".".join(list(reversed(ip.split("."))))
    c.execute("SELECT COUNT(*) FROM records WHERE domain_id=%s AND name=%s",
                  (DOMAIN, "{}.{}".format(reversedip, DOMAIN_NAME)))
    exists = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM whitelist WHERE ip=%s",
                  (ip,))
    whitelisted = c.fetchone()[0]
    if exists == 0 and whitelisted == 0:
        c.execute("""INSERT INTO records (domain_id, name, type, content, ttl, change_date, ordername, auth) VALUES
                   (%s, %s, 'A', '127.0.0.2', 300, %s, %s, 1)""",
                  (DOMAIN, "{}.{}".format(reversedip, DOMAIN_NAME), int(time.time()), ip.replace(".", " ")))
    conn.commit()
    conn.close()

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
