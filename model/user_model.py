import mysql.connector
import json
from flask import make_response

class user_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="******123**",
                database="Flask_tutorial"
            )
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary = True)
            print("connection Successful")
        except Exception as e:
            print("some error", e)

    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        print(result)
        if len(result)>0:
           res = make_response({"payload": result}, 200)
           res.headers['Access-control-Allow-Origin'] = '*'
           return res
        else:
            return  make_response({"message": "No data Found"}, 404)
        
    def user_addone_model(self, data):
       try:
          query = """
          INSERT INTO users(name,email,phone,role,passward)
          VALUES(%s,%s,%s,%s,%s)
          """

          values = (
              data.get("name"),
              data.get("email"),
              data.get("phone"),
              data.get("role"),
              data.get("passward")
           )

          self.cur.execute(query, values)
          self.con.commit()

          return make_response({"message": "User inserted successfully"}, 201)

       except Exception as e:
          return make_response({"error": str(e)}, 400)
    
    def user_update_model(self, data, id):
      query = """
      UPDATE users
      SET name=%s, email=%s, phone=%s, role=%s, passward=%s
      WHERE id=%s
     """

      self.cur.execute(query, (
         data.get("name"),
         data.get("email"),
         data.get("phone"),
         data.get("role"),
         data.get("passward"),
         id
        ))

      self.con.commit()
      return make_response({"message":"Updated Successfully"}, 200)
    
    def user_delete_model(self, id):
      query = "DELETE FROM users WHERE id=%s"

      self.cur.execute(query, (id,))
      self.con.commit()

      if self.cur.rowcount > 0:
         return make_response({"message": "User Deleted Successfully"}, 200)
      else:
         return make_response({"message": "User Not Found"}, 200)
    
    def user_patch_model(self, data, id):

      if len(data) == 0:
          return {"message": "No data provided"}

      query = "UPDATE users SET "
      values = []

      for key in data:
          query += f"{key}=%s,"
          values.append(data[key])

      # remove last comma
      query = query[:-1]

      query += " WHERE id=%s"
      values.append(id)

      print("Query:", query)
      print("Values:", values)

      self.cur.execute(query, tuple(values))
      self.con.commit()

      if self.cur.rowcount > 0:
          return {"message": "User Updated Successfully"}
      else:
          return {"message": "No User Found"}
      
    def user_pagination_model(self, limit, page):
      try:
          limit = int(limit)
          page = int(page)

          if limit <= 0 or page <= 0:
              return make_response(
                  {"error": "page and limit must be greater than 0"},
                  400
              )

          start = limit * (page - 1)

          query = "SELECT * FROM users LIMIT %s OFFSET %s"
          self.cur.execute(query, (limit, start))

          result = self.cur.fetchall()

          return make_response({
              "page": page,
              "limit": limit,
              "payload": result
            }, 200)

      except Exception as e:
        return make_response({"error": str(e)}, 400)

