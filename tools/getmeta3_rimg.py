#!/bin/bash
#

# Function

# Choose-img

img1=$1
img=$2

# Mount
starttime=`date +'%Y-%m-%d %H:%M:%S'`
umount $img >/dev/null 2>&1
rm -rf ./$img >/dev/null 2>&1
mkdir $img
rm -rf ./symlinks-$img
rm -rf ./file_contexts3-$img
rm -rf ./fs_config-$img
mount -r $img1 $img/ >/dev/null 2>&1

if [[ ! $(ls ./$img/) ]]; then
  echo Mount $img1 fail1!
  exit 1 
else
  echo Compiled by XiaoWan...
  echo Mount ext4 image...
fi

# symlinks
if [[ $(find ./$img -type l) ]]; then
echo Create symlinks-$img...
 for line in $(find ./$img -type l); do
  sudo ls -al $line |grep ">" | while read line; do
      echo ${line##*  } | while read line; do
              echo ${line#* } | while read line; do          
                     OIFS=$IFS; IFS="  "; set -- $line; sym=$1;files=$3; IFS=$OIFS 
                        printf "symlink(\"$files\", \"$sym\");" >>symlinks-$img; printf "\\n" >>symlinks-$img
                   done
             done 
       done
 done
sed -i 's/\.\//\//' symlinks-$img
else 
echo No symlinks find in $img...
fi

# file_contexts3
echo Create file_contexts-$img...
for line in $(sudo find ./$img** | grep "$img"); do
OIFS=$IFS; IFS=" "; set -- $(sudo ls -Zd $line |grep "\.\/$img"); con=$1;files=$2; IFS=$OIFS 
echo $files $con >>file_contexts3-$img
done
if [ -d "./$img/system/app" ];then
        sed -i 's/.\{8\}//' file_contexts3-$img
          else
           sed -i 's/.\{1\}//' file_contexts3-$img
     fi
     
# fs_config
echo Create fs_config-$img...
for file in $(find $img** | grep "$img"); do
    uid=$(stat -c %u $file)
    gid=$(stat -c %g $file)
    fs=$(stat -c %a $file)
    printf "$file $uid $gid 0$fs" >>fs_config-$img
    printf "\\n" >>fs_config-$img
done
if [ -d "./$img/system/app" ];then
        sed -i 's/.\{7\}//' fs_config-$img
     fi

# Finish
echo Umount $img...
umount $img >/dev/null 2>&1
endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "Finish (total :$((end_seconds-start_seconds))"s")"
rm -rf ./$img >/dev/null 2>&1
sort -bdf symlinks-$img -o symlinks-$img >/dev/null 2>&1
sort -bdf file_contexts3-$img -o file_contexts3-$img >/dev/null 2>&1
sort -bdf fs_config-$img -o fs_config-$img >/dev/null 2>&1


