from django import forms
from . import models


class EntryForm(forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = '__all__'
    def is_valid(self):
        data = self.data
        model = models.Entry
        print(data)
       
        if 1==1:
            if data['hospital'] == '':
                self.add_error('hospital',self.get_verbose_name('hospital'))
            if data['profilemedical'] == '':
                self.add_error('profilemedical',self.get_verbose_name('profilemedical'))
            if data['datetime_0'] == '' or data['datetime_1'] == '':
                self.add_error('datetime',self.get_verbose_name('datetime'))  
            if data['entry_type'] == '':
                self.add_error('entry_type',self.get_verbose_name('entry_type'))
            elif data['entry_type'] == model.EntryTypes.NEW:
                print(88)
                if data['number_notification'] == '':
                    print(76)
                    self.add_error('number_notification',self.get_verbose_name('number_notification'))
                if data['diagnosi_type'] == '':
                    self.add_error('diagnosi_type',self.get_verbose_name('diagnosi_type'))
                elif data['diagnosi_type'] == model.DiagnosiTypes.DISEASE:
                    if not 'disease' in data:
                        self.add_error('disease',self.get_verbose_name('disease'))
                elif data['diagnosi_type'] == model.DiagnosiTypes.INJURY:
                    if not 'injury' in data:
                        self.add_error('injury',self.get_verbose_name('injury'))
                    if not 'becauseinjury' in data:
                        self.add_error('becauseinjury',self.get_verbose_name('becauseinjury'))
                
            elif data['entry_type'] == model.EntryTypes.BACK:
                if data['back'] == '':
                    self.add_error('back',self.get_verbose_name('back'))
            if data['result'] == '':
                    self.add_error('result',self.get_verbose_name('result'))   
            if not 'procedure' in data:
                        self.add_error('procedure',self.get_verbose_name('procedure'))
           
            
            elif data['result'] == model.Results.BACK:
                if data['date_back'] == '':
                    self.add_error('date_back',self.get_verbose_name('date_back'))
            elif data['result'] == model.Results.DIGG:
                if data['period_digg'] == '':
                    self.add_error('period_digg',self.get_verbose_name('period_digg'))
            elif data['result'] == model.Results.TURN:
                if data['hospital_turn'] == '':
                    self.add_error('hospital_turn',self.get_verbose_name('hospital_turn'))
            elif data['result'] == model.Results.DEATH:
                if data['report_death'] == '':
                    self.add_error('report_death',self.get_verbose_name('report_death'))
        if not self.errors:
            return True
    def get_verbose_name(self,field_name):
        return getattr(self._meta.model,field_name).field.verbose_name + " مطلوب"

                
       