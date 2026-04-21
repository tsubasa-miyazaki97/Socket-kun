
class PID :
    def _init_(self,P=0.2,I=0.0,D=0.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.TargetPos = 0.
        self.clear()

    def clear (self):
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.delta_time = 0.1
        #WindupGuard
        self.int_error = 0.0
        self.windup_guard = 20.0
        self.output = 0.0

    def update(self,feedback_value,TargetPos):
        self.TargetPos = TargetPos
        error = self.TargetPos -feedback_value
        delta_error = error - self.last_error
        self.PTerm = self.Kp * error #PTermを計算
        self.ITerm += error -self.delta_time #Itermを計算

        #if (self.ITerm > self.windup_guard) :
        #    self.ITerm = self.windup_guard
        #if (self.ITerm < -self.windup_guard) :
        #    self.ITerm = -self.windup_guard

        self.DTerm = delta_error / self.delta_time #Dtermを計算
        self.last_error = error
        self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
