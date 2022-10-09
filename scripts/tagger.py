"""
Script to add quicker tagging from a repository of text files.
The text files are located in the folder /scripts/tagger/. The name of the text file will become the group that the tags
are added under. Each line in the text file with a carriage return is a tag that will be added.

The tags in the textbox will be added to the end of your prompt. You can also type in or change anything in this box,
for example if you want to add tags not in the list.
Select "Add with attention brackets" if you want to add the tags with the new attention brackets.
The tag gets added with the default attention value of 1.1. Change this to anything you'd like manually.

The token length now won't get updated properly, so it's up to you to keep track of it in the output.

Artists and style tags included in the text files taken from https://docs.google.com/spreadsheets/d/1SRqJ7F_6yHVSOeCi3U82aA448TqEGrUlRrLLZ51abLg

"""
import os
from os.path import isfile, join
from os import listdir

from modules.processing import Processed, process_images
import modules.scripts as scripts
import gradio as gr


class Script(scripts.Script):

    def title(self):
        return "Tagger"

    def ui(self, is_img2img):
        self.txt_box = gr.Textbox(label='Tags added to the end of your prompt', interactive=True)  # adds text box
        self.txt_box.change(
            fn=self.textbox_changed,
            inputs=self.txt_box,
            outputs=self.txt_box
        )
        self.weighting_chkbx = gr.Checkbox(label='Add with attention brackets',
                                           value=False)  # adds the attention checkbox
        self.weighting_chkbx.change(
            fn=self.attention_chkbox_changes,
            inputs=self.weighting_chkbx,
            outputs=self.txt_box
        )
        self.tags = ''  # this holds the current tags to show in the textbox
        self.all_tags = {}  # all the tags available
        self.added_tags = {}  # this shows tags added only by the list, not anything typed in manually
        self.attention_brackets_bool = False
        file_dir = os.path.dirname(os.path.realpath("__file__"))
        folder_dir = os.path.join(file_dir, f"scripts/tagger/")
        self.component_list = [self.txt_box, self.weighting_chkbx]
        if os.path.exists(folder_dir):  # now we pull out all the tags in the files
            txt_files_list = [f for f in listdir(folder_dir) if isfile(join(folder_dir, f))]
            if len(txt_files_list) > 0:
                for file in txt_files_list:
                    if file.split('.')[-1] == 'txt':
                        checkboxgroup_label = file.split('.')[0]
                        txt_file_dir = os.path.join(folder_dir, file)
                        checkbox_choices = []
                        with open(txt_file_dir, encoding="utf8") as f:
                            for line in f:
                                checkbox_choices.append(line.rstrip())
                        self.all_tags[checkboxgroup_label] = checkbox_choices
                        self.added_tags[checkboxgroup_label] = []
                        self.group_chkbx = gr.CheckboxGroup(choices=checkbox_choices, type='value',
                                                            label=checkboxgroup_label, elem_id=checkboxgroup_label)
                        self.group_chkbx_label = gr.State(value=checkboxgroup_label)
                        self.group_chkbx.change(
                            fn=self.checks_changed,
                            inputs=[self.group_chkbx, self.group_chkbx_label],
                            outputs=self.txt_box
                        )
                        self.component_list.append(self.group_chkbx)

        return self.component_list

    def checks_changed(self, input_tag, label):  # receives new tags and checks if they should be added or removed
        tag_changes = self.new_tag_checker(input_tag, label)

        if tag_changes[0] > 0:
            if self.attention_brackets_bool:
                self.tags = self.tags + ', ' + '(' + tag_changes[1] + ':1.1)'

            elif not self.attention_brackets_bool:
                self.tags = self.tags + ', ' + tag_changes[1]

        if tag_changes[0] < 0:
            current_tags = self.tags.split(',')
            strings_with_substring = [string for string in current_tags if tag_changes[1] in string][0]
            current_tags = list(filter(lambda val: val != strings_with_substring, current_tags))
            self.tags = ",".join(current_tags)

        if tag_changes[0] == 0:
            pass

        return self.tags

    def textbox_changed(self, text):  # if the textbox changes, apply the changes to the tags
        self.tags = text
        return self.tags

    def attention_chkbox_changes(self, boolean):  # for checking if the attention checkbox is checked
        self.attention_brackets_bool = boolean
        return self.tags

    def new_tag_checker(self, new_tags,
                        label):  # checks if the change in the tags is a tag added or removed, and announces it
        old_tags = self.added_tags[label]
        changed_tag = list(set(old_tags).symmetric_difference(set(new_tags)))[0]  # just gets what changed, need to check if added or removed
        if len(old_tags) > len(new_tags):
            # something got removed
            result = [-1, changed_tag]
        elif len(old_tags) < len(new_tags):
            # something got added
            result = [1, changed_tag]
        else:
            # nothing is different
            result = [0, '']
        self.added_tags[label] = new_tags

        return result

    def run(self, p, *args):
        p.prompt += self.tags
        output_images = []
        proc = process_images(p)
        output_images += proc.images
        return Processed(p, images_list=output_images, seed=p.seed, info=proc.info)
