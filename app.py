from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from collections import defaultdict
from collections import OrderedDict
from datetime import datetime

app = Flask(__name__)

dbconn = None
connection = None


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
                                         password=connect.dbpass, host=connect.dbhost, \
                                         database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/currentjobs", methods=['GET'])
def currentjobs():
    connection = getCursor()
    connection.execute("""
        SELECT `job`.`job_id`, `job`.`customer`, `customer`.`family_name`, `job`.`job_date`
        FROM `job` LEFT JOIN `customer` ON `job`.`customer` = `customer`.`customer_id`
        WHERE `job`.`completed` = 0;
    """)
    jobList = connection.fetchall()
    return render_template("currentjoblist.html", job_list=jobList)


@app.route("/job/<job_id>", methods=['GET', 'POST'])
def job(job_id):
    connection = getCursor()
    serviceId2Name = defaultdict(str)
    serviceId2Qty = defaultdict(int)
    partId2Name = defaultdict(str)
    partId2Qty = defaultdict(int)
    if request.method == "GET":
        job_dct = {"job_id": job_id}
        connection.execute("""
            SELECT `job`.`job_id`, `job`.`completed`, `job_service`.`service_id`, `job_service`.`qty`, `job_part`.`part_id`, `job_part`.`qty`
            FROM  `job` 
            LEFT JOIN `job_service` ON `job`.`job_id` = `job_service`.`job_id`
            LEFT JOIN `job_part` ON `job_part`.`job_id` = `job`.`job_id`
            WHERE `job`.`job_id` = %s;
        """, (job_id,))
        jobList = connection.fetchall()
        if len(jobList) == 0:
            return redirect(url_for('currentjobs'))
        job_dct["completed"] = jobList[0][1]

        connection.execute("""
            SELECT `service`.`service_id`, `service`.`service_name`
            FROM `service`;
            """)
        serviceList = connection.fetchall()
        for service in serviceList:
            serviceId2Name[service[0]] = service[1]
            serviceId2Qty[service[0]] = 0

        connection.execute("""
            SELECT `part`.`part_id`, `part`.`part_name`
            FROM `part`;
            """)
        partList = connection.fetchall()
        for part in partList:
            partId2Name[part[0]] = part[1]
            partId2Qty[part[0]] = 0

        for job in jobList:
            if job[2] is not None:
                serviceId2Qty[job[2]] = job[3]
            if job[4] is not None:
                partId2Qty[job[4]] = job[5]
        return render_template("job.html", job=job_dct, serviceId2Name=serviceId2Name, serviceId2Qty=serviceId2Qty,
                               partId2Name=partId2Name, partId2Qty=partId2Qty)
    elif request.method == "POST":
        # 获取所有的Payload
        payload = request.form.to_dict()
        for key in payload:
            if key.startswith("service_"):
                service_id = key[8:]
                qty = payload[key]
                connection.execute("""
                    INSERT INTO `job_service`
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE `qty` = %s;
                """, (job_id, service_id, qty, qty))
            elif key.startswith("part_"):
                part_id = key[5:]
                qty = payload[key]
                connection.execute("""
                    INSERT INTO `job_part`
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE `qty` = %s;
                """, (job_id, part_id, qty, qty))
        if payload["completed"] == "1":
            serviceId2Price = defaultdict(int)
            partId2Price = defaultdict(int)
            connection.execute("""
                SELECT `service`.`service_id`, `service`.`cost`
                FROM `service`;
                """)
            servicePriceList = connection.fetchall()
            for service in servicePriceList:
                serviceId2Price[str(service[0])] = float(service[1])
            connection.execute("""
                SELECT `part`.`part_id`, `part`.`cost`
                FROM `part`;
                """)
            partPriceList = connection.fetchall()
            for part in partPriceList:
                partId2Price[str(part[0])] = float(part[1])
            total = 0
            for key in payload:
                if key.startswith("service_"):
                    service_id = key[8:]
                    qty = payload[key]
                    total += int(qty) * serviceId2Price[service_id]
                elif key.startswith("part_"):
                    part_id = key[5:]
                    qty = payload[key]
                    total += int(qty) * partId2Price[part_id]
            connection.execute("""
                UPDATE `job`
                SET `completed` = 1, `total_cost` = %s
                WHERE `job_id` = %s;
            """, (total, job_id))
        return redirect(url_for('currentjobs'))


@app.route("/customerlist", methods=['GET'])
def customerlist():
    connection = getCursor()
    connection.execute("""
        SELECT `customer`.*
        FROM `customer`
        ORDER BY `customer`.`family_name`, `customer`.`first_name`;
    """)
    customerList = connection.fetchall()
    return render_template("customerlist.html", customer_list=customerList)


@app.route("/customer/search", methods=['POST'])
def customersearch():
    connection = getCursor()
    payload = request.form.to_dict()
    connection.execute("""
        SELECT `customer`.*
        FROM `customer`
        WHERE `customer`.`family_name` LIKE %s OR `customer`.`first_name` LIKE %s
        ORDER BY `customer`.`family_name`, `customer`.`first_name`;
    """, ("%" + payload["search"] + "%", "%" + payload["search"] + "%"))
    customerList = connection.fetchall()
    return render_template("customerlist.html", customer_list=customerList)


@app.route("/customer/add", methods=['POST'])
def customeradd():
    connection = getCursor()
    payload = request.form.to_dict()
    connection.execute("""
        INSERT INTO `customer` (`family_name`, `first_name`, `phone`, `email`)
        VALUES (%s, %s, %s, %s);
    """, (payload["family_name"], payload["first_name"], payload["phone"], payload["email"]))
    return redirect(url_for('customerlist'))


@app.route("/service/list", methods=['GET'])
def servicelist():
    connection = getCursor()
    connection.execute("""
        SELECT `service`.*
        FROM `service`;
    """)
    serviceList = connection.fetchall()
    return render_template("servicelist.html", service_list=serviceList)


@app.route("/service/add", methods=['POST'])
def serviceadd():
    connection = getCursor()
    payload = request.form.to_dict()
    connection.execute("""
        INSERT INTO `service` (`service_name`, `cost`)
        VALUES (%s, %s);
    """, (payload["service_name"], payload["cost"]))
    return redirect(url_for('servicelist'))


@app.route("/part/list", methods=['GET'])
def partlist():
    connection = getCursor()
    connection.execute("""
        SELECT `part`.*
        FROM `part`;
    """)
    partList = connection.fetchall()
    return render_template("partlist.html", part_list=partList)


@app.route("/part/add", methods=['POST'])
def partadd():
    connection = getCursor()
    payload = request.form.to_dict()
    connection.execute("""
        INSERT INTO `part` (`part_name`, `cost`)
        VALUES (%s, %s);
    """, (payload["part_name"], payload["cost"]))
    return redirect(url_for('partlist'))


@app.route("/job/list", methods=['GET'])
def joblist():
    connection = getCursor()
    connection.execute("""
        SELECT `job`.*
        FROM `job`;
    """)
    jobList = connection.fetchall()
    min_date = datetime.now().strftime('%Y-%m-%d')
    connection.execute("""
    SELECT `customer`.`customer_id`, `customer`.`first_name`
    FROM `customer`;
    """)
    customers = connection.fetchall()
    return render_template("joblist.html", job_list=jobList, min_date=min_date, customers=customers)


@app.route("/job/add", methods=['POST'])
def jobschedule():
    connection = getCursor()
    payload = request.form.to_dict()
    connection.execute("""
        INSERT INTO `job` (`job_date`, `customer`)
        VALUES (%s, %s);
    """, (payload["job_date"], payload["customer"]))
    return redirect(url_for('joblist'))


@app.route("/unpaid_bill/list", methods=['GET'])
def unpaid_bill_list():
    connection = getCursor()
    connection.execute("""
        SELECT `customer`.`customer_id`, `customer`.`first_name`, `customer`.`family_name`, `job`.`job_id`, `job`.`job_date`, `job`.`total_cost`, `job`.`completed`
        FROM `customer` LEFT JOIN `job` ON `customer`.`customer_id` = `job`.`customer`
        WHERE `job`.`paid` = 0
        ORDER BY `job`.`job_date`, `customer`.`customer_id`;
        """)
    unpaid_bills_list = connection.fetchall()
    return render_template("unpaid_bill_list.html", unpaid_bill_list=unpaid_bills_list)


@app.route("/unpaid/search", methods=['POST'])
def unpaid_search():
    connection = getCursor()
    payload = request.form.to_dict()
    connection.execute("""
        SELECT `customer`.`customer_id`, `customer`.`first_name`, `customer`.`family_name`, `job`.`job_id`, `job`.`job_date`, `job`.`total_cost`, `job`.`completed`
        FROM `customer` LEFT JOIN `job` ON `customer`.`customer_id` = `job`.`customer`
        WHERE `job`.`paid` = 0 AND (`customer`.`family_name` LIKE %s OR `customer`.`first_name` LIKE %s)
        ORDER BY `job`.`job_date`, `customer`.`customer_id`;
        """, ("%" + payload["search"] + "%", "%" + payload["search"] + "%"))
    unpaid_bills_list = connection.fetchall()
    return render_template("unpaid_bill_list.html", unpaid_bill_list=unpaid_bills_list)


@app.route("/unpaid/update/<job_id>", methods=['GET'])
def unpaid_update(job_id):
    connection = getCursor()
    connection.execute("""
        UPDATE `job`
        SET `paid` = 1
        WHERE `job_id` = %s;
        """, (job_id,))
    return redirect(url_for('unpaid_bill_list'))


@app.route("/bill_history/list", methods=['GET'])
def bill_history():
    connection = getCursor()
    connection.execute("""
    SELECT `customer`.`customer_id`, `customer`.`first_name`, `customer`.`family_name`, `customer`.`email`, `customer`.`phone`
    FROM `customer`
    ORDER BY `customer`.`family_name`, `customer`.`first_name`;
    """)
    order_customers = connection.fetchall()
    bill_history_dct = OrderedDict()
    for customer in order_customers:
        customer_id = customer[0]
        connection.execute("""
        SELECT `job`.`job_id`, `job`.`job_date`, `job`.`total_cost`, `job`.`completed`, `job`.`paid`
        FROM `job`
        WHERE `job`.`customer` = %s
        ORDER BY `job`.`job_date` DESC;
        """, (customer_id,))
        bill_list = connection.fetchall()
        bill_list_flag = []
        for bill in bill_list:
            bill = list(bill)
            red_flag = False
            if bill[4] == 0:
                job_date = bill[1]
                if (datetime.date(datetime.now()) - job_date).days > 14:
                    red_flag = True
            bill.append(red_flag)
            bill_list_flag.append(bill)
        bill_history_dct[customer] = bill_list_flag
    return render_template("bill_history_list.html", bill_history_dct=bill_history_dct)


if __name__ == '__main__':
    getCursor()
    app.run(debug=True)

