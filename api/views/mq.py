from rest_framework import viewsets

class MQViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        super(MQViewSet, self).__init__(*args, **kwargs)
        model_name = self.__class__.__name__.lower()
        self.post_topic_key = "model." + model_name + ".post";
        self.update_topic_key = "model." + model_name + ".update";
        self.delete_topic_key = "model." + model_name + ".delete";

    def on_create(self, serializer):
        print "SERIALIZER: %s" % serializer.data
        print self.post_topic_key

#        channel.basic_publish(exchange='whyd',
#                              routing_key=self.post_topic_key,
#                              body=serializer.data)

    def on_update(self, serializer):
        print "SERIALIZER: %s" % serializer.data
        print self.update_topic_key

#        channel.basic_publish(exchange='whyd',
#                              routing_key=self.update_topic_key,
#                              body=serializer.data)

    def on_destroy(self, instance):
        print "DELETE INSTANCE: %s" % instance.id
        print self.delete_topic_key

#        channel.basic_publish(exchange='whyd',
#                              routing_key=self.delete_topic_key,
#                              body=serializer.data)
    
    def perform_create(self, serializer):
        super(MQViewSet, self).perform_create(serializer)
        self.on_create(serializer)

    def perform_update(self, serializer):
        super(MQViewSet, self).perform_update(serializer)
        self.on_update(serializer)

    def perform_destroy(self, serializer):
        super(MQViewSet, self).perform_destroy(serializer)
        self.on_destroy(serializer)
