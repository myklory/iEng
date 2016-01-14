#!/usr/bin/env python
# encoding: utf-8

from werkzeug.security import check_password_hash

class User():
  def __init__(self, nickname):
    self.nickname = nickname

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.nickname


  @staticmethod
  def validate_login(password_hash, password):
    return check_password_hash(password_hash, password)
