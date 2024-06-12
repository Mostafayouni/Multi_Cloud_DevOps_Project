
region = "us-east-1"


vpc_cidr = "10.0.0.0/16"


subnet = { 
      subnet_cidr       = "10.0.0.0/24"
      availability_zone = "us-east-1a" 
      }
     
#EC2 module value
public_key_path = "~/.ssh/ivolve-key.pem.pub"
ec2_ami_id 	= "ami-0975ad60e5054592a" 
ec2_type  	= "m4.large"

#CloudWatch module value
sns_email = "mostafayounis053@gmail.com"
