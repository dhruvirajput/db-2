from flask import Flask, render_template, request, jsonify, session

from db import read, insert_update

app = Flask(__name__)

app.secret_key = "myKey"


@app.route('/')
def index():
    users = read("SELECT * FROM [dbo].[User]")
    roles = read("SELECT * FROM [dbo].[Role]")
    privileges = read("SELECT * FROM [dbo].[Privilege]")
    access = read("SELECT * FROM [dbo].[Access]")
    tables = read("SELECT * FROM [dbo].[Table]")
    return render_template("index.html", users=users, roles=roles, privileges=privileges, access=access, tables=tables)


@app.route('/user', methods=['POST'])
def user():
    name = request.form['Name']
    u_name = request.form['UName']
    password = request.form['Password']
    address = request.form['Address']
    phone = request.form['PhoneNo']

    id_query = "SELECT TOP (1) UID FROM [USER] ORDER BY UID DESC"
    u_id = insert_update("INSERT INTO [User] (Name, UName, Password, Address, PhoneNo) VALUES (?, ?, ?, ?, ?)",
                         id_query, (name, u_name, password, address, phone))
    if u_id:
        session['UID'] = u_id
        return jsonify({'count': u_id, 'Status_Code': 200})
    else:
        return jsonify({'Status_Code': 500, 'Message': 'Internal Error.'})


@app.route('/role', methods=['POST'])
def role():
    name = request.form['RName']
    description = request.form['Description']

    id_query = "SELECT TOP (1) RID FROM [Role] ORDER BY RID DESC"
    r_id = insert_update("INSERT INTO [Role] (RName, Description) VALUES (?, ?)", id_query, (name, description))

    if r_id:
        session['RID'] = r_id
        if insert_update("UPDATE [User] SET RID = ? WHERE UID = ?", id_query, (r_id, str(session['UID']))):
            return jsonify({'count': r_id, 'Status_Code': 200})

    return jsonify({'Status_Code': 500, 'Message': 'Internal Error.'})


@app.route('/table', methods=['POST'])
def table():
    name = request.form['TName']

    id_query = "SELECT TOP (1) TID FROM [Table] ORDER BY TID DESC"
    t_id = insert_update("INSERT INTO [Table] (TName, UID) VALUES (?, ?)", id_query, (name, str(session['UID'])))

    if t_id:
        session['TID'] = t_id
        return jsonify({'count': t_id, 'Status_Code': 200})

    return jsonify({'Status_Code': 500, 'Message': 'Internal Error.'})


@app.route('/privilege', methods=['POST'])
def privilege():
    name = request.form['PName']
    privilege_type = request.form['PrivilegeType']

    id_query = "SELECT TOP (1) PID FROM [Privilege] ORDER BY PID DESC"
    p_id = insert_update("INSERT INTO [Privilege] (PName, PrivilegeType) VALUES (?, ?)", id_query,
                         (name, privilege_type))

    if p_id:
        session['PID'] = p_id
        if insert_update("INSERT INTO [Access] (RID, TID, PID, IsAccess) VALUES (?, ?, ?, ?)", id_query,
                         (str(session['RID']), str(session['TID']), str(p_id), 1)):
            return jsonify({'count': p_id, 'Status_Code': 200})

    return jsonify({'Status_Code': 500, 'Message': 'Internal Error.'})


@app.route('/get-privilege-role', methods=['POST'])
def get_privilege_role():
    name = request.form['Role']

    data = read("SELECT * FROM [Privilege] WHERE PID IN "
                "(SELECT PID FROM [Access] WHERE RID IN "
                "(SELECT RID FROM [Role] WHERE RName='" + str(name) + "'))")

    if data:
        return jsonify({'Records': data, 'Status_Code': 200})

    return jsonify({'Status_Code': 500, 'Message': 'Internal Error.'})


@app.route('/get-privilege-user', methods=['POST'])
def get_privilege_user():
    name = request.form['UName']

    data = read("SELECT * FROM [Privilege] WHERE PID IN "
                "(SELECT PID FROM [Access] WHERE RID IN "
                "(SELECT RID FROM [USER] WHERE UName='" + str(name) + "'))")

    if data:
        return jsonify({'Records': data, 'Status_Code': 200})

    return jsonify({'Status_Code': 500, 'Message': 'Internal Error.'})


@app.route('/check-privilege-user', methods=['POST'])
def check_privilege_user():
    name = request.form['UName']
    privilege_type = request.form['PrivilegeType']

    data = read("SELECT COUNT(PID) FROM [Privilege] WHERE PID IN (SELECT PID FROM [Access] WHERE RID IN "
                "(SELECT RID FROM [USER] WHERE UName='" + str(name) +
                "')) AND PrivilegeType='" + str(privilege_type) + "'")

    if int(data[0]['']) > 0:
        return jsonify({'Result': True, 'Status_Code': 200})
    elif int(data[0]['']) <= 0:
        return jsonify({'Result': False, 'Status_Code': 200})
    else:
        return jsonify({'Status_Code': 500, 'Message': 'Internal Error.'})


if __name__ == '__main__':
    app.run(debug=True)
